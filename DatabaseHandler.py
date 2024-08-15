import sqlite3
import os.path


def create_database():
    db_name = 'FilmPortal.db'

    # Vérifie si le fichier de la base de données existe déjà
    test_presence = os.path.isfile(db_name)

    # Si la base de données n'existe pas, la créer et configurer le schéma
    if not test_presence:
        conn = sqlite3.connect(db_name)  # Crée ou se connecte à la base de données
        cursor = conn.cursor()

        # Ouvre et lit le fichier SQL pour créer le schéma
        with open('FilmPortal.sql', 'r') as sql_file:
            sql_script = sql_file.read()

        cursor.executescript(sql_script)  # Exécute le script SQL pour créer les tables, etc.
        conn.commit()  # Valide les modifications dans la base de données
        conn.close()  # Ferme la connexion à la base de données

    else:
        # Si la base de données existe, se connecte simplement à celle-ci
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

    # Vous pouvez ajouter du code supplémentaire ici pour travailler avec la base de données, si nécessaire


# Appelle la fonction pour créer la base de données si nécessaire
create_database()
