import sqlite3

conn = sqlite3.connect("hotel.db")
cursor = conn.cursor()

# Table Hotel
cursor.execute("""
CREATE TABLE IF NOT EXISTS Hotel (
    id INTEGER PRIMARY KEY,
    ville TEXT,
    pays TEXT,
    code_postal INTEGER
)
""")
cursor.executemany("INSERT INTO Hotel VALUES (?, ?, ?, ?)", [
    (1, 'Paris', 'France', 75001),
    (2, 'Lyon', 'France', 69002)
])

# Table Client
cursor.execute("""
CREATE TABLE IF NOT EXISTS Client (
    id INTEGER PRIMARY KEY,
    adresse TEXT,
    ville TEXT,
    code_postal INTEGER,
    email TEXT,
    telephone TEXT,
    nom TEXT
)
""")
cursor.executemany("INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)", [
    (1, '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
    (2, '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
    (3, '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
    (4, '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
    (5, '3 Rue des Fleurs', 'Nice', 6000, 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')
])

# Table Prestation
cursor.execute("""
CREATE TABLE IF NOT EXISTS Prestation (
    id INTEGER PRIMARY KEY,
    prix INTEGER,
    description TEXT
)
""")
cursor.executemany("INSERT INTO Prestation VALUES (?, ?, ?)", [
    (1, 15, 'Petit-déjeuner'),
    (2, 30, 'Navette aéroport'),
    (3, 0, 'Wi-Fi gratuit'),
    (4, 50, 'Spa et bien-être'),
    (5, 20, 'Parking sécurisé')
])

# Table TypeChambre
cursor.execute("""
CREATE TABLE IF NOT EXISTS TypeChambre (
    id INTEGER PRIMARY KEY,
    nom TEXT,
    prix REAL
)
""")
cursor.executemany("INSERT INTO TypeChambre VALUES (?, ?, ?)", [
    (1, 'Simple', 80),
    (2, 'Double', 120)
])

# Table Chambre
cursor.execute("""
CREATE TABLE IF NOT EXISTS Chambre (
    id INTEGER PRIMARY KEY,
    numero INTEGER,
    etage INTEGER,
    fumeur INTEGER,
    type_chambre_id INTEGER,
    hotel_id INTEGER,
    FOREIGN KEY (type_chambre_id) REFERENCES TypeChambre(id),
    FOREIGN KEY (hotel_id) REFERENCES Hotel(id)
)
""")
cursor.executemany("INSERT INTO Chambre VALUES (?, ?, ?, ?, ?, ?)", [
    (1, 201, 2, 0, 1, 1),
    (2, 502, 5, 1, 1, 2),
    (3, 305, 3, 0, 2, 1),
    (4, 410, 4, 0, 2, 2),
    (5, 104, 1, 1, 2, 2),
    (6, 202, 2, 0, 1, 1),
    (7, 307, 3, 1, 1, 2),
    (8, 101, 1, 0, 1, 1)
])

cursor.execute("""
CREATE TABLE IF NOT EXISTS Reservation (
    id INTEGER PRIMARY KEY,
    date_debut TEXT,
    date_fin TEXT,
    client_id INTEGER,
    FOREIGN KEY (client_id) REFERENCES Client(id)
)
""")
cursor.executemany("INSERT INTO Reservation VALUES (?, ?, ?, ?)", [
    (1, '2025-06-15', '2025-06-18', 1),
    (2, '2025-07-01', '2025-07-05', 2),
    (3, '2025-08-10', '2025-08-14', 3),
    (4, '2025-09-05', '2025-09-07', 4),
    (5, '2025-09-20', '2025-09-25', 5),
    (7, '2025-11-12', '2025-11-14', 2),
    (9, '2026-01-15', '2026-01-18', 4),
    (10, '2026-02-01', '2026-02-05', 2)
])


cursor.execute("""
CREATE TABLE IF NOT EXISTS ChambreReservation (
    chambre_id INTEGER,
    reservation_id INTEGER,
    PRIMARY KEY (chambre_id, reservation_id),
    FOREIGN KEY (chambre_id) REFERENCES Chambre(id),
    FOREIGN KEY (reservation_id) REFERENCES Reservation(id)
)
""")
cursor.executemany("INSERT INTO ChambreReservation VALUES (?, ?)", [
    (1, 1), (2, 2), (3, 3), (4, 4),
    (5, 5), (6, 7), (7, 9), (8, 10)
])

cursor.execute("""
CREATE TABLE IF NOT EXISTS Evaluation (
    id INTEGER PRIMARY KEY,
    date TEXT,
    note INTEGER,
    commentaire TEXT,
    client_id INTEGER,
    FOREIGN KEY (client_id) REFERENCES Client(id)
)
""")
cursor.executemany("INSERT INTO Evaluation VALUES (?, ?, ?, ?, ?)", [
    (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
    (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
    (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
    (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
    (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
])

conn.commit()
conn.close()

print("✅ Base de données hotel.db créée avec succès.")
