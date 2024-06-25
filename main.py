import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class MovieDatabaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FilmPortal : outil de recherche cinématographique")
        self.geometry("1250x750")


        self.connection = sqlite3.connect("FilmPortal.db")
        self.cursor = self.connection.cursor()

        self.create_widgets()

    def search_movies(self):
        titre = self.entry_titre.get()
        realisateur = self.entry_realisateur.get()
        acteur = self.entry_acteur.get()
        boite_production = self.entry_boite_production.get()

        sql = """
        SELECT film.id, film.nom_film, film.date_sortie, realisateur.nom_realisateur, 
               boite_production.nom_boite_production, 
               GROUP_CONCAT(acteur.nom_acteur, ', ') as acteurs, film.synopsis
        FROM film
        LEFT JOIN realisateur ON film.realisateur_id = realisateur.id
        LEFT JOIN boite_production ON film.boite_production_id = boite_production.id
        LEFT JOIN film_acteur ON film.id = film_acteur.film_id
        LEFT JOIN acteur ON film_acteur.acteur_id = acteur.id
        WHERE film.nom_film LIKE ? AND realisateur.nom_realisateur LIKE ? 
              AND acteur.nom_acteur LIKE ? AND boite_production.nom_boite_production LIKE ?
        GROUP BY film.id, film.nom_film, film.date_sortie, realisateur.nom_realisateur, 
                 boite_production.nom_boite_production, film.synopsis
        """

        titre = f"%{titre}%"
        realisateur = f"%{realisateur}%"
        acteur = f"%{acteur}%"
        boite_production = f"%{boite_production}%"

        self.cursor.execute(sql, (titre, realisateur, acteur, boite_production))
        results = self.cursor.fetchall()
        print(results)
        for row in self.tree.get_children():
            self.tree.delete(row)

        for result in results:
            self.tree.insert("", tk.END, values=result)

        if not results:
            messagebox.showinfo("Aucun résultat", "Aucun film trouvé.")

    def add_movie(self):
        nom_film = self.entry_nom_film.get()
        date_sortie = self.entry_date_sortie.get()
        realisateur_id = self.entry_realisateur_id.get()
        boite_production_id = self.entry_boite_production_id.get()
        synopsis = self.entry_synopsis.get("1.0", tk.END)

        if not (nom_film and date_sortie and realisateur_id and boite_production_id):
            messagebox.showwarning("Champ manquant", "Veuillez remplir tous les champs obligatoires.")
            return

        sql = """
        INSERT INTO film (nom_film, date_sortie, realisateur_id, boite_production_id, synopsis)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (nom_film, date_sortie, realisateur_id, boite_production_id, synopsis))
        self.connection.commit()
        messagebox.showinfo("Succès", "Film ajouté avec succès.")
        self.clear_entries()

    def update_movie(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sélection manquante", "Veuillez sélectionner un film à mettre à jour.")
            return

        item = self.tree.item(selected_item)
        movie_id = item["values"][0]
        nom_film = self.entry_nom_film.get()
        date_sortie = self.entry_date_sortie.get()
        realisateur_id = self.entry_realisateur_id.get()
        boite_production_id = self.entry_boite_production_id.get()
        synopsis = self.entry_synopsis.get("1.0", tk.END)

        if not (nom_film and date_sortie and realisateur_id and boite_production_id):
            messagebox.showwarning("Champ manquant", "Veuillez remplir tous les champs obligatoires.")
            return

        sql = """
        UPDATE film
        SET nom_film = ?, date_sortie = ?, realisateur_id = ?, boite_production_id = ?, synopsis = ?
        WHERE id = ?
        """
        self.cursor.execute(sql, (nom_film, date_sortie, realisateur_id, boite_production_id, synopsis, movie_id))
        self.connection.commit()
        messagebox.showinfo("Succès", "Film mis à jour avec succès.")
        self.clear_entries()

    def delete_movie(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Sélection manquante", "Veuillez sélectionner un film à supprimer.")
            return

        item = self.tree.item(selected_item)
        movie_id = item["values"][0]

        sql = "DELETE FROM film WHERE id = ?"
        self.cursor.execute(sql, (movie_id,))
        self.connection.commit()
        messagebox.showinfo("Succès", "Film supprimé avec succès.")
        self.search_movies()

    def clear_entries(self):
        self.entry_nom_film.delete(0, tk.END)
        self.entry_date_sortie.delete(0, tk.END)
        self.entry_realisateur_id.delete(0, tk.END)
        self.entry_boite_production_id.delete(0, tk.END)
        self.entry_synopsis.delete("1.0", tk.END)

    def create_widgets(self):
        frame_search = ttk.LabelFrame(self, text="Recherche de films", padding=(20, 10))
        frame_search.grid(row=0, column=0, padx=20, pady=10, sticky="ew")

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

        ttk.Label(frame_form, text="ID du Réalisateur:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.entry_realisateur_id = ttk.Entry(frame_form)
        self.entry_realisateur_id.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="ID de la Boîte de Production:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.entry_boite_production_id = ttk.Entry(frame_form)
        self.entry_boite_production_id.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_form, text="Synopsis:").grid(row=4, column=0, padx=5, pady=5, sticky="nw")
        self.entry_synopsis = tk.Text(frame_form, height=5)
        self.entry_synopsis.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        frame_buttons = ttk.Frame(frame_form)
        frame_buttons.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")
        frame_buttons.columnconfigure((0, 1, 2), weight=1)

        self.button_add = ttk.Button(frame_buttons, text="Ajouter", command=self.add_movie)
        self.button_add.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.button_update = ttk.Button(frame_buttons, text="Mettre à jour", command=self.update_movie)
        self.button_update.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.button_delete = ttk.Button(frame_buttons, text="Supprimer", command=self.delete_movie)
        self.button_delete.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        frame_results = ttk.LabelFrame(self, text="Résultats", padding=(20, 10))
        frame_results.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
        frame_results.columnconfigure(0, weight=1)
        frame_results.rowconfigure(0, weight=1)

        columns = ("id", "nom_film", "date_sortie", "nom_realisateur", "nom_boite_production", "acteurs", "synopsis")
        self.tree = ttk.Treeview(frame_results, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, minwidth=50, width=100)

        self.scrollbar = ttk.Scrollbar(frame_results, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=self.scrollbar.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

if __name__ == "__main__":
    app = MovieDatabaseApp()
    app.mainloop()
