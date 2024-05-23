import tkinter as tk
from tkinter import ttk
import sqlite3
from ttkbootstrap import Style
import os

# Nom de votre base de données
nom_base_de_donnees = 'movies.db'

# Obtenez le chemin absolu du répertoire contenant votre script Python
chemin_script = os.path.dirname(os.path.abspath(__file__))

# Chemin absolu vers la base de données
chemin_absolu_base_de_donnees = os.path.join(chemin_script, nom_base_de_donnees)

# Connexion à la base de données en spécifiant le chemin absolu
conn = sqlite3.connect(chemin_absolu_base_de_donnees)
cursor = conn.cursor()

class MovieDatabaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FilmPortal : movie finder assistant")
        self.geometry("750x500")

        self.style = Style(theme="darkly")

        # Connexion à la base de données SQLite
        self.connection = sqlite3.connect("movies.db")
        self.cursor = self.connection.cursor()

        self.create_widgets()

    def search_movies(self):
        # Méthode pour rechercher des films
        titre = self.entry_titre.get()
        realisateur = self.entry_realisateur.get()
        acteur = self.entry_acteur.get()
        boite_production = self.entry_boite_production.get()

        sql = "SELECT * FROM Film WHERE "
        conditions = []
        parameters = []

        if titre:
            conditions.append("Titre LIKE ?")
            parameters.append(f"%{titre}%")
        if realisateur:
            conditions.append("Realisateur LIKE ?")
            parameters.append(f"%{realisateur}%")
        if acteur:
            conditions.append("Acteur LIKE ?")
            parameters.append(f"%{acteur}%")
        if boite_production:
            conditions.append("BoiteProduction LIKE ?")
            parameters.append(f"%{boite_production}%")

        if conditions:
            sql += " AND ".join(conditions)
        else:
            sql = "SELECT * FROM Film"  # No search criteria, fetch all

        try:
            self.cursor.execute(sql, parameters)
            rows = self.cursor.fetchall()

            for child in self.treeview.get_children():
                self.treeview.delete(child)

            for row in rows:
                self.treeview.insert("", "end", values=row)
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")

    def create_widgets(self):
        # Méthode pour créer les widgets de l'interface utilisateur
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.grid(column=0, row=0, padx=0, pady=0, sticky=tk.W)

        label_titre = ttk.Label(left_frame, text="Titre du Film:")
        label_titre.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        self.entry_titre = ttk.Entry(left_frame)
        self.entry_titre.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

        label_realisateur = ttk.Label(left_frame, text="Réalisateur:")
        label_realisateur.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        self.entry_realisateur = ttk.Entry(left_frame)
        self.entry_realisateur.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)

        label_acteur = ttk.Label(left_frame, text="Acteurs:")
        label_acteur.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

        self.entry_acteur = ttk.Entry(left_frame)
        self.entry_acteur.grid(column=1, row=2, padx=5, pady=5, sticky=tk.W)

        label_boite_production = ttk.Label(left_frame, text="Nom de la boîte de production:")
        label_boite_production.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)

        self.entry_boite_production = ttk.Entry(left_frame)
        self.entry_boite_production.grid(column=1, row=3, padx=5, pady=5, sticky=tk.W)

        search_button = ttk.Button(left_frame, text="Chercher", command=self.search_movies)
        search_button.grid(column=0, row=4, columnspan=2, pady=10, sticky=tk.W)

        right_frame = ttk.Frame(main_frame)
        right_frame.grid(column=1, row=0, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        columns = ("ID", "Titre", "Date de Sortie", "Réalisateur", "Boîte de Production", "Synopsis")
        self.treeview = ttk.Treeview(right_frame, columns=columns, show="headings", height=14)

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor=tk.CENTER)

        self.treeview.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)

        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.treeview.yview)
        self.treeview.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=tk.N + tk.S)

    def on_closing(self):
        # Close the database connection
        if self.connection:
            self.connection.close()
        self.destroy()


if __name__ == "__main__":
    app = MovieDatabaseApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
