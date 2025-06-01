import streamlit as st
import sqlite3
from datetime import datetime, timedelta
import base64
import os

# Couleurs
PRIMARY = "#287094"
SECONDARY = "#D4D4CE"
BG = "#F6F6F6"
DARK = "#023246"

# Fonction pour lire l'image en base64
def get_img_as_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Connexion DB
def connect_db():
    return sqlite3.connect("hotel.db")

# Configuration de la page
st.set_page_config(page_title="Gestion Hôtel", layout="wide")

# Charger image de fond
if os.path.exists("hotel_bg.jpg"):
    img_bg = get_img_as_base64("hotel_bg.jpg")
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_bg}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .main-title {{
            background-color: rgba(255, 255, 255, 0.8);
            border-radius: 10px;
            text-align: center;
            padding: 20px;
            margin: 20px auto;
            width: 80%;
        }}
        .main-title h1 {{
            color: {DARK};
            font-size: 3rem;
            margin-bottom: 0.2rem;
        }}
        .main-title p {{
            font-size: 1.1rem;
            color: {PRIMARY};
        }}
        .stDataFrame th, .stDataFrame td {{
            border: 2px solid {PRIMARY} !important;
            text-align: center;
        }}
        </style>
    """, unsafe_allow_html=True)

# Menu latéral
menu = st.sidebar.selectbox("Menu", [
    "Accueil",
    "Liste des réservations",
    "Liste des clients",
    "Chambres disponibles",
    "Ajouter un client",
    "Ajouter une réservation"
])

# Page d'accueil avec fond
if menu == "Accueil":
    st.markdown(f"""
    <div class="main-title">
        <h1>Gestion des Réservations Hôtelières</h1>
        <p>Application web pour gérer les clients, réservations et chambres d’un hôtel – Réalisée avec SQLite, Python et Streamlit.</p>
    </div>
    """, unsafe_allow_html=True)

# Réservations
elif menu == "Liste des réservations":
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.id, c.nom, r.date_debut, r.date_fin, ch.numero
        FROM Reservation r
        JOIN Client c ON r.client_id = c.id
        JOIN ChambreReservation cr ON cr.reservation_id = r.id
        JOIN Chambre ch ON cr.chambre_id = ch.id
    """)
    reservations = cursor.fetchall()
    st.subheader("📅 Réservations")
    if reservations:
        st.dataframe(reservations, use_container_width=True)
    else:
        st.warning("Aucune réservation trouvée.")
    conn.close()

# Clients
elif menu == "Liste des clients":
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Client")
    clients = cursor.fetchall()
    st.subheader("👤 Clients")
    if clients:
        st.dataframe(clients, use_container_width=True)
    else:
        st.warning("Aucun client trouvé.")
    conn.close()

# Chambres disponibles
elif menu == "Chambres disponibles":
    st.subheader("🛏 Chambres disponibles entre deux dates")
    date_debut = st.date_input("Date de début")
    date_fin = st.date_input("Date de fin")
    if date_debut >= date_fin:
        st.warning("❗ La date de début doit être avant la date de fin.")
    elif st.button("Rechercher"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM Chambre WHERE id NOT IN (
                SELECT chambre_id FROM ChambreReservation cr
                JOIN Reservation r ON cr.reservation_id = r.id
                WHERE NOT (r.date_fin < ? OR r.date_debut > ?)
            )
        """, (date_debut, date_fin))
        chambres = cursor.fetchall()
        if chambres:
            st.dataframe(chambres, use_container_width=True)
        else:
            st.info("Aucune chambre disponible pour cette période.")
        conn.close()

# Ajouter un client
elif menu == "Ajouter un client":
    st.subheader("➕ Ajouter un client")
    nom = st.text_input("Nom")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    code_postal = st.text_input("Code postal")
    email = st.text_input("Email")
    telephone = st.text_input("Téléphone")
    if st.button("Valider"):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Client (adresse, ville, code_postal, email, telephone, nom) VALUES (?, ?, ?, ?, ?, ?)",
                       (adresse, ville, code_postal, email, telephone, nom))
        conn.commit()
        conn.close()
        st.success("Client ajouté avec succès ✅")

# Ajouter une réservation
elif menu == "Ajouter une réservation":
    st.subheader("📅 Nouvelle réservation")
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, nom FROM Client")
    clients = cursor.fetchall()
    client = st.selectbox("Choisir un client", clients, format_func=lambda x: x[1])

    date_debut = st.date_input("Date de début")
    date_fin = st.date_input("Date de fin", value=date_debut + timedelta(days=3))

    if date_fin <= date_debut:
        st.error("❗ La date de fin doit être strictement après la date de début.")

    cursor.execute("""
        SELECT * FROM Chambre WHERE id NOT IN (
            SELECT chambre_id FROM ChambreReservation cr
            JOIN Reservation r ON cr.reservation_id = r.id
            WHERE NOT (r.date_fin < ? OR r.date_debut > ?)
        )
    """, (date_debut, date_fin))
    disponibles = cursor.fetchall()

    if disponibles:
        chambre = st.selectbox("Choisir une chambre disponible", disponibles, format_func=lambda x: f"Chambre {x[1]} (Hôtel {x[5]})")
    else:
        st.info("Aucune chambre disponible pour cette période.")

    if st.button("Réserver"):
        if date_fin <= date_debut:
            st.warning("Impossible de réserver : la date de fin doit être après la date de début.")
        elif not disponibles:
            st.warning("Impossible de réserver : aucune chambre disponible pour cette période.")
        else:
            cursor.execute("INSERT INTO Reservation (date_debut, date_fin, client_id) VALUES (?, ?, ?)",
                           (date_debut, date_fin, client[0]))
            reservation_id = cursor.lastrowid
            cursor.execute("INSERT INTO ChambreReservation (chambre_id, reservation_id) VALUES (?, ?)",
                           (chambre[0], reservation_id))
            conn.commit()
            conn.close()
            st.success("✅ Réservation enregistrée avec succès")
