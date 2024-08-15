-- Création de la table genre
CREATE TABLE genre (
    id INTEGER PRIMARY KEY,
    nom_genre VARCHAR(255) NOT NULL
);

-- Création de la table realisateur
CREATE TABLE realisateur (
    id INTEGER PRIMARY KEY,
    nom_realisateur VARCHAR(255) NOT NULL
);

-- Création de la table acteur
CREATE TABLE acteur (
    id INTEGER PRIMARY KEY,
    nom_acteur VARCHAR(255) NOT NULL
);

-- Création de la table boite_production
CREATE TABLE boite_production (
    id INTEGER PRIMARY KEY,
    nom_boite_production VARCHAR(255) NOT NULL
);

-- Création de la table film
CREATE TABLE film (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom_film VARCHAR(255) NOT NULL,
    date_sortie DATE,
    synopsis TEXT
);

-- Création de la table film_realisateur
CREATE TABLE film_realisateur (
    film_id INTEGER,
    realisateur_id INTEGER,
    PRIMARY KEY (film_id, realisateur_id),
    FOREIGN KEY (film_id) REFERENCES film(id),
    FOREIGN KEY (realisateur_id) REFERENCES realisateur(id)
);

-- Création de la table film_genre
CREATE TABLE film_genre (
    film_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (film_id, genre_id),
    FOREIGN KEY (film_id) REFERENCES film(id),
    FOREIGN KEY (genre_id) REFERENCES genre(id)
);

-- Création de la table film_boite_production
CREATE TABLE film_boite_production (
    film_id INTEGER,
    boite_production_id INTEGER,
    PRIMARY KEY (film_id, boite_production_id),
    FOREIGN KEY (film_id) REFERENCES film(id),
    FOREIGN KEY (boite_production_id) REFERENCES boite_production(id)
);

-- Création de la table film_acteur
CREATE TABLE film_acteur (
    film_id INTEGER,
    acteur_id INTEGER,
    PRIMARY KEY (film_id, acteur_id),
    FOREIGN KEY (film_id) REFERENCES film(id),
    FOREIGN KEY (acteur_id) REFERENCES acteur(id)
);

-- Ajout de genres
INSERT INTO genre (id, nom_genre) VALUES
(1, 'action'),
(2, 'comedy'),
(3, 'drama'),
(4, 'science fiction'),
(5, 'thriller');

-- Ajout de réalisateurs
INSERT INTO realisateur (id, nom_realisateur) VALUES
(1, 'christopher nolan'),
(2, 'quentin tarantino'),
(3, 'james cameron'),
(4, 'greta gerwig'),
(5, 'steven spielberg');

-- Ajout d'acteurs
INSERT INTO acteur (id, nom_acteur) VALUES
(1, 'tom hanks'),
(2, 'leonardo dicaprio'),
(3, 'cillian murphy'),
(4, 'john travolta'),
(5, 'keanu reeves'),
(6, 'ryan gosling'),
(7, 'emma stone'),
(8, 'tim robbins'),
(9, 'stephen lang'),
(10, 'uma thurman'),
(11, 'kate winslet'),
(12, 'gary sinise'),
(13, 'carrie-anne moss'),
(14, 'christian bale'),
(15, 'heath ledger'),
(16, 'morgan freeman'),
(17, 'christoph waltz'),
(18, 'brad pitt'),
(19, 'sigourney weaver');

-- Ajout de boîtes de production
INSERT INTO boite_production (id, nom_boite_production) VALUES
(1, 'warner bros'),
(2, 'universal pictures'),
(3, 'paramount pictures'),
(4, '20th century fox'),
(5, 'sony pictures');


-- Ajout de films
INSERT INTO film (id, nom_film, date_sortie, synopsis) VALUES
(1, 'Inception', '2010-07-16',  'Dom Cobb is a skilled thief who steals valuable secrets by infiltrating the subconscious of his targets while they dream.'),
(2, 'Pulp Fiction', '1994-10-14',  'The intertwined stories of several criminals in Los Angeles collide in unexpected ways.'),
(3, 'Titanic', '1997-12-19', 'The love story of Jack and Rose, two members of different social classes, aboard the legendary Titanic.'),
(4, 'La La Land', '2016-12-09', 'A love story between a passionate jazz musician and an aspiring actress in Los Angeles.'),
(5, 'The Matrix', '1999-03-31', 'A hacker named Neo discovers the truth about the simulated reality he lives in.'),
(6, 'Forrest Gump', '1994-07-06', 'The extraordinary story of Forrest Gump, a man with a low IQ, but who has witnessed significant historical moments in the United States.'),
(7, 'The Dark Knight', '2008-07-18', 'Batman faces the Joker, a psychotic criminal who seeks to create chaos in Gotham City.'),
(8, 'The Shawshank Redemption', '1994-09-10', 'The touching story of the friendship between two inmates sentenced to life at Shawshank prison.'),
(9, 'Inglourious Basterds', '2009-05-20', 'During World War II, a group of Jewish-American soldiers known as the Basterds targets Nazis.'),
(10, 'Avatar', '2009-12-18', 'On the moon Pandora, a paraplegic marine is sent on a diplomatic mission but gets involved in a conflict between humans and the Navi, an alien race.');

-- Associer des genres aux films
INSERT INTO film_genre (film_id, genre_id) VALUES
(1, 3), -- Inception (Drama)
(2, 3), -- Pulp Fiction (Drama)
(3, 3), -- Titanic (Drama)
(6, 3), -- Forrest Gump (Drama)
(7, 1), -- The Dark Knight (Action)
(7, 3), -- The Dark Knight (Drama)
(8, 3), -- The Shawshank Redemption (Drama)
(9, 1), -- Inglourious Basterds (Action)
(10, 4); -- Avatar (Science Fiction)

-- Associer des acteurs aux films
INSERT INTO film_acteur (film_id, acteur_id) VALUES
(1, 2), -- Inception (Leonardo DiCaprio)
(1, 3), -- Inception (Cillian Murphy)
(2, 4), -- Pulp Fiction (John Travolta)
(2, 10), -- Pulp Fiction (Uma Thurman)
(3, 2), -- Titanic (Leonardo DiCaprio)
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

-- Associer des boite de production aux films
INSERT INTO film_boite_production (film_id, boite_production_id) VALUES
(1, 3),
(2, 2),
(3, 5),
(6, 3),
(7, 1),
(7, 3),
(8, 3),
(9, 1),
(10, 4);

-- Associer des realisateurs aux films
INSERT INTO film_realisateur (film_id, realisateur_id) VALUES
(1, 2),
(2, 5),
(3, 3),
(6, 3),
(7, 1),
(7, 3),
(8, 3),
(9, 1),
(10, 4);

