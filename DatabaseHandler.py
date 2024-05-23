import os
import sqlite3

# Nom de votre base de données
nom_base_de_donnees = 'films.db'

# Obtenez le chemin absolu du répertoire contenant votre script Python
chemin_script = os.path.dirname(os.path.abspath(__file__))

# Chemin absolu vers la base de données
chemin_absolu_base_de_donnees = os.path.join(chemin_script, nom_base_de_donnees)

# Connexion à la base de données en spécifiant le chemin absolu
conn = sqlite3.connect(chemin_absolu_base_de_donnees)
cursor = conn.cursor()