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

        self.create_widgets() # Méthode pour créer les widgets de l'interface graphique

        # gestion db
        self.connection = sqlite3.connect("FilmPortal.db") # Connexion à la base de données SQLite
        self.cursor = self.connection.cursor()# Création d'un curseur pour exécuter des commandes SQL



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
        if not (nom_film and date_sortie and realisateurs and boites_production and genres and acteurs and synopsis):
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
        self.connection.commit() # Sauvegarde des changements

        film_id = self.cursor.lastrowid # Récupération de l'ID du film ajouté

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

        ## Ajout des boîtes de production associées
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

        messagebox.showinfo("Succès", "Film ajouté avec succès.")
        self.clear_entries()

    def update_movie(self):
        selected_item = self.tree.selection() # Récupération de l'élément sélectionné
        if not selected_item:
            messagebox.showwarning("Sélection manquante", "Veuillez sélectionner un film à mettre à jour.")
            return

        # Récupération des valeurs entrées par l'utilisateur pour la mise à jour
        item = self.tree.item(selected_item)
        movie_id = item["values"][0]
        nom_film = self.entry_nom_film.get()
        date_sortie = self.entry_date_sortie.get()
        realisateurs = self.entry_realisateurs.get()
        genres = self.entry_genres.get()
        boites_production = self.entry_boites_production.get()
        acteurs = self.entry_acteurs.get()
        synopsis = self.entry_synopsis.get("1.0", tk.END).strip()


        if (nom_film or date_sortie or synopsis):
            sql = "UPDATE film SET "
            parameters = []

            # List to hold individual SET clauses
            set_clauses = []

            # Add conditions to the SET clause based on the presence of the values
            if nom_film:
                set_clauses.append("nom_film = ?")
                parameters.append(nom_film)

            if date_sortie:
                set_clauses.append("date_sortie = ?")
                parameters.append(date_sortie)

            if synopsis and len(synopsis) != 0:
                print(len(synopsis))
                print(f"s= {synopsis}")

                set_clauses.append("synopsis = ?")
                parameters.append(synopsis)

            # Join the clauses and add the WHERE condition
            sql += ", ".join(set_clauses) + " WHERE id = ?"
            print(sql)
            parameters.append(movie_id)

            # Execute the query if there are any SET clauses
            if set_clauses:
                self.cursor.execute(sql, parameters)
                self.connection.commit()

        if realisateurs:
            noms_realisateur = [i.lower() for i in realisateurs.split(',') if i]
            sql_realisateur = ','.join(['?' for i in noms_realisateur])
            sql = f"SELECT id FROM realisateur WHERE nom_realisateur IN ({sql_realisateur})"
            self.cursor.execute(sql, noms_realisateur)
            realisateur_ids = [row[0] for row in self.cursor.fetchall()]

            if not realisateur_ids:
                messagebox.showwarning("Valeur non trouvée", "Valeur non trouvée pour le champ realisateur")
                return

            sql = f"DELETE FROM film_realisateur WHERE film_id = {movie_id}"
            self.cursor.execute(sql)

            for realisateur_id in realisateur_ids:
                sql = """
                INSERT INTO film_realisateur (film_id, realisateur_id)
                VALUES (?, ?)
                """
                self.cursor.execute(sql, (movie_id, realisateur_id))
                self.connection.commit()

        if genres:
            noms_genres = [i.lower() for i in genres.split(',') if i]
            sql_genre = ','.join(['?' for i in noms_genres])
            sql = f"SELECT id FROM genre WHERE nom_genre IN ({sql_genre})"
            self.cursor.execute(sql, noms_genres)
            genre_ids = [row[0] for row in self.cursor.fetchall()]

            if not genre_ids:
                messagebox.showwarning("Valeur non trouvée", "Valeur non trouvée pour le champ genre")
                return

            sql = f"DELETE FROM film_genre WHERE film_id = {movie_id}"
            self.cursor.execute(sql)

            for genre_id in genre_ids:
                sql = """
                INSERT INTO film_genre (film_id, genre_id)
                VALUES (?, ?)
                """
                self.cursor.execute(sql, (movie_id, genre_id))
                self.connection.commit()

        if boites_production:
            noms_boites_production = [i.lower() for i in boites_production.split(',') if i]
            sql_boites_production = ','.join(['?' for i in noms_boites_production])
            sql = f"SELECT id FROM boite_production WHERE nom_boite_production IN ({sql_boites_production})"
            self.cursor.execute(sql, noms_boites_production)
            boites_production_ids = [row[0] for row in self.cursor.fetchall()]

            if not boites_production_ids:
                messagebox.showwarning("Valeur non trouvée", "Valeur non trouvée pour le champ boites de production")
                return

            sql = f"DELETE FROM film_boite_production WHERE film_id = {movie_id}"
            self.cursor.execute(sql)

            for boite_production_id in boites_production_ids:
                sql = """
                INSERT INTO film_boite_production (film_id, boite_production_id)
                VALUES (?, ?)
                """
                self.cursor.execute(sql, (movie_id, boite_production_id))
                self.connection.commit()

        if acteurs:
            noms_acteur = [i.lower() for i in acteurs.split(',') if i]
            sql_acteur = ','.join(['?' for i in noms_acteur])
            sql = f"SELECT id FROM acteur WHERE nom_acteur IN ({sql_acteur})"
            self.cursor.execute(sql, noms_acteur)
            acteur_ids = [row[0] for row in self.cursor.fetchall()]

            if not acteur_ids:
                messagebox.showwarning("Valeur non trouvée", "Valeur non trouvée pour le champ acteur")
                return

            sql = f"DELETE FROM film_acteur WHERE film_id = {movie_id}"
            self.cursor.execute(sql)

            for acteur_id in acteur_ids:
                sql = """
                INSERT INTO film_acteur (film_id, acteur_id)
                VALUES (?, ?)
                """
                self.cursor.execute(sql, (movie_id, acteur_id))
                self.connection.commit()

        messagebox.showinfo("Succès", "Film mis à jour avec succès.")
        self.clear_entries()

    def delete_movie(self):
        selected_item = self.tree.selection() # Récupération de l'élément sélectionné
        if not selected_item:
            messagebox.showwarning("Sélection manquante", "Veuillez sélectionner un film à supprimer.")
            return

        item = self.tree.item(selected_item)
        # Récupération de l'ID du film à partir de l'élément sélectionné
        movie_id = item["values"][0]

        # Suppression film de table film
        sql = "DELETE FROM film WHERE id = ?"
        self.cursor.execute(sql, (movie_id,))
        self.connection.commit()

        # supprime film de table film
        sql = "DELETE FROM film_realisateur WHERE film_id = ?"
        self.cursor.execute(sql, (movie_id,))
        self.connection.commit()

        # supprime film de table film
        sql = "DELETE FROM film_genre WHERE film_id = ?"
        self.cursor.execute(sql, (movie_id,))
        self.connection.commit()

        # supprime film de table film
        sql = "DELETE FROM film_boite_production WHERE film_id = ?"
        self.cursor.execute(sql, (movie_id,))
        self.connection.commit()

        # supprime film de table film
        sql = "DELETE FROM film_acteur WHERE film_id = ?"
        self.cursor.execute(sql, (movie_id,))
        self.connection.commit()

        # Nettoyage du formulaire et mise à jour de l'affichage des films
        messagebox.showinfo("Succès", "Film supprimé avec succès.")
        self.search_movies()

    def clear_entries(self):
        # Réinitialisation des champs de saisie du formulaire
        self.entry_nom_film.delete(0, tk.END)
        self.entry_date_sortie.delete(0, tk.END)
        self.entry_realisateurs.delete(0, tk.END)
        self.entry_acteurs.delete(0, tk.END)
        self.entry_genres.delete(0, tk.END)
        self.entry_boites_production.delete(0, tk.END)
        self.entry_synopsis.delete("1.0", tk.END)

    def create_widgets(self):
        # Création des widgets pour les champs de saisie et les boutons
        frame_search = ttk.LabelFrame(self, text="Recherche de films", padding=(20, 10))
        frame_search.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

        # Champs de saisie pour les détails du film
        ttk.Label(frame_search, text="Titre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_titre = ttk.Entry(frame_search)
        self.entry_titre.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_search, text="Réalisateur:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_realisateur = ttk.Entry(frame_search)
        self.entry_realisateur.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_search, text="Acteur:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_acteur = ttk.Entry(frame_search)
        self.entry_acteur.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_search, text="Boîte de Production:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_boite_production = ttk.Entry(frame_search)
        self.entry_boite_production.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.button_search = ttk.Button(frame_search, text="Rechercher", command=self.search_movies)
        self.button_search.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        frame_form = ttk.LabelFrame(self, text="Formulaire de film", padding=(20, 10))
        frame_form.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        ttk.Label(frame_form, text="Nom du film:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_nom_film = ttk.Entry(frame_form)
        self.entry_nom_film.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="Date de sortie (YYYY-MM-DD):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_date_sortie = ttk.Entry(frame_form)
        self.entry_date_sortie.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="Réalisateur(s):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_realisateurs = ttk.Entry(frame_form)
        self.entry_realisateurs.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="Genre(s):").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_genres = ttk.Entry(frame_form)
        self.entry_genres.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="Boîte(s) de Production:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.entry_boites_production = ttk.Entry(frame_form)
        self.entry_boites_production.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="Acteur(s):").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.entry_acteurs = ttk.Entry(frame_form)
        self.entry_acteurs.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="Synopsis:").grid(row=6, column=0, padx=5, pady=5, sticky="nw")
        self.entry_synopsis = tk.Text(frame_form, height=5)
        self.entry_synopsis.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        frame_buttons = ttk.Frame(frame_form)
        frame_buttons.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
        frame_buttons.columnconfigure((0, 1, 2), weight=1)

        # Boutons pour ajouter, mettre à jour ou supprimer un film
        self.button_add = ttk.Button(frame_buttons, text="Ajouter", command=self.add_movie)
        self.button_add.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.button_update = ttk.Button(frame_buttons, text="Mettre à jour", command=self.update_movie)
        self.button_update.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.button_delete = ttk.Button(frame_buttons, text="Supprimer", command=self.delete_movie)
        self.button_delete.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        frame_results = ttk.LabelFrame(self, text="Résultats", padding=(20, 10))
        frame_results.grid(row=5, column=0, padx=10, pady=10, sticky="nsew")
        frame_results.columnconfigure(0, weight=1)
        frame_results.rowconfigure(0, weight=1)

        # Création du Treeview pour afficher les résultats de recherche
        columns = ("Id", "Film", "Date sortie", "Genres", "Acteurs", "Realisateurs", "Boites production", "Synopsis")
        self.tree = ttk.Treeview(frame_results, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=50, width=100)

        # Barre de défilement pour le Treeview
        self.scrollbar = ttk.Scrollbar(frame_results, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)


if __name__ == "__main__":
    create_database() # Création de la base de données si elle n'existe pas
    app = MovieDatabaseApp() # Instanciation de l'application
    app.mainloop() # Lancement de la boucle principale de l'application
