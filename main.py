import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import *
import sqlite3
from DatabaseHandler import create_database

class MovieDatabaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FilmPortal : outil de recherche cinématographique")
        self.geometry("1250x750")

        self.create_widgets()  # Méthode pour créer les widgets de l'interface graphique

        # Connexion à la base de données SQLite
        self.connection = sqlite3.connect("FilmPortal.db")
        self.cursor = self.connection.cursor()  # Création d'un curseur pour exécuter des commandes SQL

    def search_movies(self):
        # Récupération des valeurs entrées par l'utilisateur pour la recherche
        titre = self.entry_titre.get()
        realisateur = self.entry_realisateur.get()
        acteur = self.entry_acteur.get()
        boite_production = self.entry_boite_production.get()

        # Requête SQL de base pour rechercher des films
        sql = """
        SELECT f.id, f.nom_film, f.date_sortie, f.synopsis
        FROM film f
        LEFT JOIN film_realisateur fr ON f.id = fr.film_id
        LEFT JOIN realisateur r ON fr.realisateur_id = r.id
        LEFT JOIN film_boite_production fb ON f.id = fb.film_id
        LEFT JOIN boite_production b ON fb.boite_production_id = b.id
        LEFT JOIN film_acteur fa ON f.id = fa.film_id
        LEFT JOIN acteur a ON fa.acteur_id = a.id
        WHERE 1=1
        """

        # Liste des paramètres pour les conditions de recherche
        params = []

        # Ajout de conditions à la requête SQL si les champs sont renseignés
        if titre:
            sql += ' AND f.nom_film LIKE ?'
            params.append(f'%{titre.lower()}%')

        if realisateur:
            sql += ' AND r.nom_realisateur LIKE ?'
            params.append(f'%{realisateur.lower()}%')

        if boite_production:
            sql += ' AND b.nom_boite_production LIKE ?'
            params.append(f'%{boite_production}%')

        if acteur:
            sql += ' AND a.nom_acteur LIKE ?'
            params.append(f'%{acteur.lower()}%')

        # Exécution de la requête principale
        self.cursor.execute(sql, params)
        movies = self.cursor.fetchall()  # Récupération des résultats de la recherche

        films = []

        # Pour chaque film trouvé, récupération des acteurs, genres, boîtes de production et réalisateurs associés
        for movie in movies:
            movie_id = movie[0]

            # Récupération des acteurs associés
            self.cursor.execute("""
            SELECT a.nom_acteur
            FROM film_acteur fa
            JOIN acteur a ON fa.acteur_id = a.id
            WHERE fa.film_id = ?
            """, (movie_id,))
            actors = [row[0] for row in self.cursor.fetchall()]
            actor_list = ', '.join(actors)

            # Récupération des genres associés
            self.cursor.execute("""
            SELECT g.nom_genre
            FROM film_genre fg
            JOIN genre g ON fg.genre_id = g.id
            WHERE fg.film_id = ?
            """, (movie_id,))
            genres = [row[0] for row in self.cursor.fetchall()]
            genre_list = ', '.join(genres)

            # Récupération des boîtes de production associées
            self.cursor.execute("""
            SELECT bp.nom_boite_production
            FROM film_boite_production fbp
            JOIN boite_production bp ON fbp.boite_production_id = bp.id
            WHERE fbp.film_id = ?
            """, (movie_id,))
            boites_production = [row[0] for row in self.cursor.fetchall()]
            boite_production_list = ', '.join(boites_production)

            # Récupération des réalisateurs associés
            self.cursor.execute("""
            SELECT r.nom_realisateur
            FROM film_realisateur fr
            JOIN realisateur r ON fr.realisateur_id = r.id
            WHERE fr.film_id = ?
            """, (movie_id,))
            realisateurs = [row[0] for row in self.cursor.fetchall()]
            realisateur_list = ', '.join(realisateurs)

            # Ajout des détails du film à la liste des résultats
            films.append((movie_id, movie[1], movie[2], genre_list, actor_list, realisateur_list, boite_production_list, movie[3]))

        # Nettoyage des anciens résultats dans l'interface graphique
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Affichage des résultats dans l'interface
        for film in films:
            self.tree.insert("", tk.END, values=film)

        # Affichage d'un message si aucun film n'a été trouvé
        if not films:
            messagebox.showinfo("Aucun résultat", "Aucun film trouvé.")

    def add_movie(self):
        # Récupération des valeurs du formulaire pour ajouter un film
        nom_film = self.entry_nom_film.get()
        date_sortie = self.entry_date_sortie.get()
        realisateurs = self.entry_realisateurs.get()
        genres = self.entry_genres.get()
        boites_production = self.entry_boites_production.get()
        acteurs = self.entry_acteurs.get()
        synopsis = self.entry_synopsis.get("1.0", tk.END)

        # Vérification que tous les champs obligatoires sont remplis
        if not (nom_film and date_sortie and realisateurs and boites_production and genres et acteurs et synopsis):
            messagebox.showwarning("Champ manquant", "Veuillez remplir tous les champs obligatoires.")
            return

        # Conversion des valeurs des réalisateurs, genres, boîtes de production et acteurs en minuscules
        noms_realisateur = [i.lower() for i in realisateurs.split(',') if i]
        noms_genre = [i.lower() for i in genres.split(',') if i]
        noms_boite_production = [i.lower() for i in boites_production.split(',') if i]
        noms_acteur = [i.lower() for i in acteurs.split(',') if i]

        # Récupération des IDs des réalisateurs
        sql_realisateur = ','.join(['?' for i in noms_realisateur])
        sql = f"SELECT id FROM realisateur WHERE nom_realisateur IN ({sql_realisateur})"
        self.cursor.execute(sql, noms_realisateur)
        realisateur_ids = [row[0] for row in self.cursor.fetchall()]

        # Récupération des IDs des genres
        sql_genre = ','.join(['?' for i in noms_genre])
        sql = f"SELECT id FROM genre WHERE nom_genre IN ({sql_genre})"
        self.cursor.execute(sql, noms_genre)
        genre_ids = [row[0] for row in self.cursor.fetchall()]

        # Récupération des IDs des boîtes de production
        sql_boite_production = ','.join(['?' for i in noms_boite_production])
        sql = f"SELECT id FROM boite_production WHERE nom_boite_production IN ({sql_boite_production})"
        self.cursor.execute(sql, noms_boite_production)
        boite_production_ids = [row[0] for row in self.cursor.fetchall()]

        # Récupération des IDs des acteurs
        sql_acteur = ','.join(['?' for i in noms_acteur])
        sql = f"SELECT id FROM acteur WHERE nom_acteur IN ({sql_acteur})"
        self.cursor.execute(sql, noms_acteur)
        acteur_ids = [row[0] for row in self.cursor.fetchall()]

        # Vérification que tous les IDs nécessaires sont récupérés
        if not (realisateur_ids and genre_ids and boite_production_ids and acteur_ids):
            messagebox.showwarning("Champ incorrect", "Veuillez verifier l'orthographe du/des realisateur(s), genre(s), boite(s) de production, acteur(s).")
            return

        # Ajout du film dans la table "film"
        sql = """
        INSERT INTO film (nom_film, date_sortie, synopsis)
        VALUES (?, ?, ?)
        """
        self.cursor.execute(sql, (nom_film, date_sortie, synopsis))
        self.connection.commit()  # Sauvegarde des changements

        film_id = self.cursor.lastrowid  # Récupération de l'ID du film ajouté

        # Ajout des réalisateurs associés
        for realisateur_id in realisateur_ids:
            sql = """
            INSERT INTO film_realisateur (film_id, realisateur_id)
            VALUES (?, ?)
            """
            self.cursor.execute(sql, (film_id, realisateur_id))
            self.connection.commit()

        # Ajout du genre associé
        for genre_id in genre_ids:
            sql = """
            INSERT INTO film_genre (film_id, genre_id)
            VALUES (?, ?)
            """
            self.cursor.execute(sql, (film_id, genre_id))
            self.connection.commit()

        # Ajout des boîtes de production associées
        for boite_production_id in boite_production_ids:
            sql = """
            INSERT INTO film_boite_production (film_id, boite_production_id)
            VALUES (?, ?)
            """
            self.cursor.execute(sql, (film_id, boite_production_id))
            self.connection.commit()

        # Ajout des acteurs associés
        for acteur_id in acteur_ids:
            sql = """
            INSERT INTO film_acteur (film_id, acteur_id)
            VALUES (?, ?)
            """
            self.cursor.execute(sql, (film_id, acteur_id))
            self.connection.commit()

        # Efface les entrées du formulaire après l'ajout
        self.clear_entries()
        messagebox.showinfo("Succès", "Film ajouté avec succès !")

    def update_movie(self):
        # Vérification qu'un film est sélectionné dans le Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucun film sélectionné", "Veuillez sélectionner un film à mettre à jour.")
            return

        # Récupération de l'ID du film sélectionné
        film_id = self.tree.item(selected_item[0])['values'][0]

        # Récupération des nouvelles valeurs du formulaire
        nom_film = self.entry_nom_film.get()
        date_sortie = self.entry_date_sortie.get()
        synopsis = self.entry_synopsis.get("1.0", tk.END)

        # Mise à jour des informations du film dans la base de données
        sql = """
        UPDATE film
        SET nom_film = ?, date_sortie = ?, synopsis = ?
        WHERE id = ?
        """
        self.cursor.execute(sql, (nom_film, date_sortie, synopsis, film_id))
        self.connection.commit()

        # Mise à jour des réalisateurs associés (procédé similaire pour genres, boîtes de production et acteurs)
        realisateurs = self.entry_realisateurs.get().split(',')
        realisateur_ids = self.get_ids('realisateur', 'nom_realisateur', realisateurs)
        self.update_association('film_realisateur', 'realisateur_id', film_id, realisateur_ids)

        # Mise à jour des genres associés
        genres = self.entry_genres.get().split(',')
        genre_ids = self.get_ids('genre', 'nom_genre', genres)
        self.update_association('film_genre', 'genre_id', film_id, genre_ids)

        # Mise à jour des boîtes de production associées
        boites_production = self.entry_boites_production.get().split(',')
        boite_production_ids = self.get_ids('boite_production', 'nom_boite_production', boites_production)
        self.update_association('film_boite_production', 'boite_production_id', film_id, boite_production_ids)

        # Mise à jour des acteurs associés
        acteurs = self.entry_acteurs.get().split(',')
        acteur_ids = self.get_ids('acteur', 'nom_acteur', acteurs)
        self.update_association('film_acteur', 'acteur_id', film_id, acteur_ids)

        # Message de confirmation et nettoyage du formulaire
        messagebox.showinfo("Succès", "Film mis à jour avec succès !")
        self.clear_entries()
        self.search_movies()  # Mise à jour de l'affichage des films

    def delete_movie(self):
        # Vérification qu'un film est sélectionné dans le Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Aucun film sélectionné", "Veuillez sélectionner un film à supprimer.")
            return

        # Récupération de l'ID du film à supprimer
        film_id = self.tree.item(selected_item[0])['values'][0]

        # Suppression des relations du film dans les tables associatives
        tables = ['film_realisateur', 'film_genre', 'film_boite_production', 'film_acteur']
        for table in tables:
            sql = f"DELETE FROM {table} WHERE film_id = ?"
            self.cursor.execute(sql, (film_id,))
            self.connection.commit()

        # Suppression du film de la table "film"
        sql = "DELETE FROM film WHERE id = ?"
        self.cursor.execute(sql, (film_id,))
        self.connection.commit()

        # Nettoyage du formulaire et mise à jour de l'affichage des films
        self.clear_entries()
        self.search_movies()
        messagebox.showinfo("Succès", "Film supprimé avec succès !")

    def clear_entries(self):
        # Réinitialisation des champs de saisie du formulaire
        self.entry_nom_film.delete(0, tk.END)
        self.entry_date_sortie.delete(0, tk.END)
        self.entry_realisateurs.delete(0, tk.END)
        self.entry_genres.delete(0, tk.END)
        self.entry_boites_production.delete(0, tk.END)
        self.entry_acteurs.delete(0, tk.END)
        self.entry_synopsis.delete("1.0", tk.END)

    def create_widgets(self):
        # Création des widgets pour les champs de saisie et les boutons
        lbl_frame = ttk.LabelFrame(self, text="Ajouter / Mettre à jour un film")
        lbl_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Champs de saisie pour les détails du film
        ttk.Label(lbl_frame, text="Titre du film:").grid(row=0, column=0, sticky="e")
        self.entry_nom_film = ttk.Entry(lbl_frame, width=50)
        self.entry_nom_film.grid(row=0, column=1)

        ttk.Label(lbl_frame, text="Date de sortie (YYYY-MM-DD):").grid(row=1, column=0, sticky="e")
        self.entry_date_sortie = ttk.Entry(lbl_frame, width=50)
        self.entry_date_sortie.grid(row=1, column=1)

        ttk.Label(lbl_frame, text="Réalisateurs (séparés par des virgules):").grid(row=2, column=0, sticky="e")
        self.entry_realisateurs = ttk.Entry(lbl_frame, width=50)
        self.entry_realisateurs.grid(row=2, column=1)

        ttk.Label(lbl_frame, text="Genres (séparés par des virgules):").grid(row=3, column=0, sticky="e")
        self.entry_genres = ttk.Entry(lbl_frame, width=50)
        self.entry_genres.grid(row=3, column=1)

        ttk.Label(lbl_frame, text="Boîtes de production (séparées par des virgules):").grid(row=4, column=0, sticky="e")
        self.entry_boites_production = ttk.Entry(lbl_frame, width=50)
        self.entry_boites_production.grid(row=4, column=1)

        ttk.Label(lbl_frame, text="Acteurs (séparés par des virgules):").grid(row=5, column=0, sticky="e")
        self.entry_acteurs = ttk.Entry(lbl_frame, width=50)
        self.entry_acteurs.grid(row=5, column=1)

        ttk.Label(lbl_frame, text="Synopsis:").grid(row=6, column=0, sticky="ne")
        self.entry_synopsis = Text(lbl_frame, width=50, height=5)
        self.entry_synopsis.grid(row=6, column=1, pady=5)

        # Boutons pour ajouter, mettre à jour ou supprimer un film
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        ttk.Button(btn_frame, text="Ajouter Film", command=self.add_movie).grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(btn_frame, text="Mettre à jour Film", command=self.update_movie).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(btn_frame, text="Supprimer Film", command=self.delete_movie).grid(row=0, column=2, padx=5, pady=5)

        # Création du Treeview pour afficher les résultats de recherche
        self.tree = ttk.Treeview(self, columns=("ID", "Titre", "Date de sortie", "Genres", "Acteurs", "Réalisateurs", "Boîtes de production", "Synopsis"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Titre", text="Titre")
        self.tree.heading("Date de sortie", text="Date de sortie")
        self.tree.heading("Genres", text="Genres")
        self.tree.heading("Acteurs", text="Acteurs")
        self.tree.heading("Réalisateurs", text="Réalisateurs")
        self.tree.heading("Boîtes de production", text="Boîtes de production")
        self.tree.heading("Synopsis", text="Synopsis")
        self.tree.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Barre de défilement pour le Treeview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.grid(row=2, column=1, sticky="ns")

if __name__ == "__main__":
    create_database()  # Création de la base de données si elle n'existe pas
    app = MovieDatabaseApp()  # Instanciation de l'application
    app.mainloop()  # Lancement de la boucle principale de l'application
