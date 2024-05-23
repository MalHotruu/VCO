class MovieDatabaseApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Recherche de films")
        self.geometry("750x500")  # Ajustement de la taille de la fenêtre

        # Utilisation du style bootstrap
        self.style = Style(theme="lumen")

        # Connexion à la base de données (à remplacer par votre propre chemin)
        self.connection = sqlite3.connect("movies.db")
        self.cursor = self.connection.cursor()

        # Création de l'interface utilisateur
        self.create_widgets()

    def create_widgets(self):
        # Frame principale
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame pour les champs de recherche et les boutons à gauche
        left_frame = ttk.Frame(main_frame)
        left_frame.grid(column=0, row=0, padx=0, pady=0, sticky=tk.W)

        label_titre = ttk.Label(left_frame, text="Titre du Film:")
        label_titre.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        self.entry_titre = ttk.Entry(left_frame)
        self.entry_titre.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

        label_realisateur = ttk.Label(left_frame, text="Nom du Réalisateur:")
        label_realisateur.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        self.entry_realisateur = ttk.Entry(left_frame)
        self.entry_realisateur.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)

        label_acteur = ttk.Label(left_frame, text="Nom de l'Acteur:")
        label_acteur.grid(column=0, row=2, padx=5, pady=5, sticky=tk.W)

        self.entry_acteur = ttk.Entry(left_frame)
        self.entry_acteur.grid(column=1, row=2, padx=5, pady=5, sticky=tk.W)

        label_boite_production = ttk.Label(left_frame, text="Nom de la Boîte de Production:")
        label_boite_production.grid(column=0, row=3, padx=5, pady=5, sticky=tk.W)

        self.entry_boite_production = ttk.Entry(left_frame)
        self.entry_boite_production.grid(column=1, row=3, padx=5, pady=5, sticky=tk.W)

        search_button = ttk.Button(left_frame, text="Chercher", command=self.search_movies)
        search_button.grid(column=0, row=4, columnspan=2, pady=10, sticky=tk.W)

        # Treeview pour afficher les résultats de la recherche à droite
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(column=1, row=0, padx=10, pady=10, sticky=tk.W+tk.E+tk.N+tk.S)

        columns = ("ID", "Titre", "Date de Sortie", "Réalisateur", "Boîte de Production", "Synopsis")
        self.treeview = ttk.Treeview(right_frame, columns=columns, show="headings", height=14)

        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=100, anchor=tk.CENTER)

        self.treeview.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)