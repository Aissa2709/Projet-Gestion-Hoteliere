# 🏨 Application de Gestion Hôtelière

Cette application est une solution simple de gestion hôtelière, développée avec **Python**, **Streamlit** pour l'interface utilisateur, et **SQLite** pour la base de données.

## Fonctionnalités

- **Liste des réservations** : Affiche toutes les réservations avec le nom du client, l'hôtel, la chambre, les dates, etc.
- **Liste des clients** : Affiche tous les clients enregistrés avec leurs informations personnelles.
- **Recherche de chambres disponibles** : Trouve les chambres libres selon l’hôtel et les dates.
- **Ajout de clients** : Permet d’enregistrer de nouveaux clients.
- **Ajout de réservations** : Permet d’ajouter une réservation en choisissant le client, la chambre, et les dates.
- **Interface simple et intuitive** avec Streamlit.

## Base de données

Le fichier `database.py` crée automatiquement une base de données SQLite nommée `hotel.db` avec les tables suivantes :

- `Hotel` : Informations sur les hôtels
- `Client` : Données personnelles des clients
- `Chambre` : Chambres disponibles dans les hôtels
- `TypeChambre` : Types de chambres (simple, double, etc.)
- `Prestation` : Prestations proposées (Wi-Fi, petit déjeuner…)
- `Reservation` : Réservations des clients
- `ChambreReservation` : Relation entre chambres et réservations
- `Evaluation` : Avis et notes des clients


## 🎥 Vidéo de démonstration

[Cliquer ici pour voir la video d'explication](https://drive.google.com/file/d/1Egghase4fu-WpNb7nnaeNX0ZBNHyJ-Um/view?usp=sharing))

## Auteurs

- Aissa Boushib
- Hiba Bajaou

