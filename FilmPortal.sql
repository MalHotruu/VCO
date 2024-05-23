-- Création de la table Genre
CREATE TABLE Genre (
    ID INT PRIMARY KEY,
    NomGenre VARCHAR(255) NOT NULL
);

-- Création de la table Realisateur
CREATE TABLE Realisateur (
    ID INT PRIMARY KEY,
    NomRealisateur VARCHAR(255) NOT NULL
);

-- Création de la table Acteur
CREATE TABLE Acteur (
    ID INT PRIMARY KEY,
    NomActeur VARCHAR(255) NOT NULL
);

-- Création de la table BoiteProduction
CREATE TABLE BoiteProduction (
    ID INT PRIMARY KEY,
    NomBoiteProduction VARCHAR(255) NOT NULL
);

-- Création de la table Film
CREATE TABLE Film (
    ID INT PRIMARY KEY,
    NomFilm VARCHAR(255) NOT NULL,
    DateSortie DATE,
    RealisateurID INT,
    BoiteProductionID INT,
    Synopsis TEXT,
    FOREIGN KEY (RealisateurID) REFERENCES Realisateur(ID),
    FOREIGN KEY (BoiteProductionID) REFERENCES BoiteProduction(ID)
);

-- Création de la table Film_Genre
CREATE TABLE Film_Genre (
    FilmID INT,
    GenreID INT,
    PRIMARY KEY (FilmID, GenreID),
    FOREIGN KEY (FilmID) REFERENCES Film(ID),
    FOREIGN KEY (GenreID) REFERENCES Genre(ID)
);

-- Création de la table Film_Acteur
CREATE TABLE Film_Acteur (
    FilmID INT,
    ActeurID INT,
    PRIMARY KEY (FilmID, ActeurID),
    FOREIGN KEY (FilmID) REFERENCES Film(ID),
    FOREIGN KEY (ActeurID) REFERENCES Acteur(ID)
);

-- Ajout de genres
INSERT INTO Genre (ID, NomGenre) VALUES
(1, 'Action'),
(2, 'Comédie'),
(3, 'Drame'),
(4, 'Science-fiction'),
(5, 'Thriller');

-- Ajout de réalisateurs
INSERT INTO Realisateur (ID, NomRealisateur) VALUES
(1, 'Christopher Nolan'),
(2, 'Quentin Tarantino'),
(3, 'James Cameron'),
(4, 'Greta Gerwig'),
(5, 'Steven Spielberg');

-- Ajout d'acteurs
INSERT INTO Acteur (ID, NomActeur) VALUES
(1, 'Tom Hanks'),
(2, 'Leonardo DiCaprio'),
(3, 'Cillian Murphy'),
(4, 'John Travolta'),
(5, 'Keanu Reeves'),
(6, 'Ryan Gosling'),
(7, 'Emma Stone'),
(8, 'Tim Robbins'),
(9, 'Stephen Lang'),
(10, 'Uma Thurman'),
(11, 'Kate Winslet'),
(12, 'Gary Sinise'),
(13, 'Carrie-Anne Moss'),
(14, 'Christian Bale'),
(15, 'Heath Ledger'),
(16, 'Morgan Freeman'),
(17, 'Christoph Waltz'),
(18, 'Brad Pitt'),
(19, 'Sigourney Weaver');

-- Ajout de boîtes de production
INSERT INTO BoiteProduction (ID, NomBoiteProduction) VALUES
(1, 'Warner Bros.'),
(2, 'Universal Pictures'),
(3, 'Paramount Pictures'),
(4, '20th Century Fox'),
(5, 'Sony Pictures');

-- Ajout de films
INSERT INTO Film (ID, NomFilm, DateSortie, RealisateurID, BoiteProductionID, Synopsis) VALUES
(1, 'Inception', '2010-07-16', 1, 1, 'Dom Cobb est un voleur expérimenté qui vole des secrets précieux en infiltrant le subconscient de ses cibles pendant qu'elles rêvent.'),
(2, 'Pulp Fiction', '1994-10-14', 2, 2, 'Les histoires entrelacées de plusieurs criminels de Los Angeles se croisent de manière inattendue.'),
(3, 'Titanic', '1997-12-19', 5, 4, 'L\'histoire d\'amour entre Jack et Rose, deux membres de différentes classes sociales, à bord du légendaire Titanic.'),
(4, 'La La Land', '2016-12-09', 4, 3, 'Une histoire d\'amour entre un musicien de jazz passionné et une aspirante actrice à Los Angeles.'),
(5, 'The Matrix', '1999-03-31', 5, 1, 'Un pirate informatique nommé Neo découvre la vérité sur la réalité simulée dans laquelle il vit.'),
(6, 'Forrest Gump', '1994-07-06', 3, 2, 'L\'histoire extraordinaire de Forrest Gump, un homme avec un QI inférieur à la moyenne, mais qui a connu des moments historiques importants aux États-Unis.'),
(7, 'The Dark Knight', '2008-07-18', 1, 1, 'Batman affronte le Joker, un criminel psychotique qui cherche à créer le chaos à Gotham City.'),
(8, 'The Shawshank Redemption', '1994-09-10', 3, 4, 'L\'histoire émouvante de l\'amitié entre deux détenus condamnés à la prison de Shawshank.'),
(9, 'Inglourious Basterds', '2009-05-20', 2, 2, 'Pendant la Seconde Guerre mondiale, un groupe de soldats juifs américains connu sous le nom de Basterds cherche à éliminer les nazis.'),
(10, 'Avatar', '2009-12-18', 5, 4, 'Sur la lune Pandora, un marine paraplégique est envoyé en mission diplomatique, mais se retrouve impliqué dans un conflit entre les humains et les Na\'vi, une race extraterrestre.');

-- Associer des genres aux films
INSERT INTO Film_Genre (FilmID, GenreID) VALUES
(6, 3), -- Forrest Gump (Drame)
(7, 1), -- The Dark Knight (Action)
(8, 3), -- The Shawshank Redemption (Drame)
(9, 1), -- Inglourious Basterds (Action)
(10, 4); -- Avatar (Science-fiction)

-- Associer des acteurs aux films
INSERT INTO Film_Acteur (FilmID, ActeurID) VALUES
(1, 2), -- Inception (Leonardo DiCaprio)
(1, 3), -- Inception (Cillian Murphy)
(2, 4), -- Pulp Fiction (John Travolta)
(2, 10), -- Pulp Fiction (Uma Thurman)
(3, 1), -- Titanic (Leonardo DiCaprio)
(3, 11), -- Titanic (Kate Winslet)
(4, 6), -- La La Land (Ryan Gosling)
(4, 7), -- La La Land (Emma Stone)
(5, 5), -- The Matrix (Keanu Reeves)
(5, 13), -- The Matrix (Carrie-Anne Moss)
(6, 1), -- Forrest Gump (Tom Hanks)
(6, 12), -- Forrest Gump (Gary Sinise)
(7, 14), -- The Dark Knight (Christian Bale)
(7, 15), -- The Dark Knight (Heath Ledger)
(8, 16), -- The Shawshank Redemption (Morgan Freeman)
(8, 8), -- The Shawshank Redemption (Tim Robbins)
(9, 17), -- Inglourious Basterds (Christoph Waltz)
(9, 18), -- Inglourious Basterds (Brad Pitt)
(10, 19), -- Avatar (Sigourney Weaver)
(10, 9); -- Avatar (Stephen Lang)
