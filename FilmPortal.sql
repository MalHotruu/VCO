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
    id INTEGER PRIMARY KEY,
    nom_film VARCHAR(255) NOT NULL,
    date_sortie DATE,
    realisateur_id INTEGER,
    boite_production_id INTEGER,
    synopsis TEXT,
    FOREIGN KEY (realisateur_id) REFERENCES realisateur(id),
    FOREIGN KEY (boite_production_id) REFERENCES boite_production(id)
);

-- Création de la table film_genre
CREATE TABLE film_genre (
    film_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (film_id, genre_id),
    FOREIGN KEY (film_id) REFERENCES film(id),
    FOREIGN KEY (genre_id) REFERENCES genre(id)
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
(1, 'Action'),
(2, 'Comedy'),
(3, 'Drama'),
(4, 'Science Fiction'),
(5, 'Thriller');

-- Ajout de réalisateurs
INSERT INTO realisateur (id, nom_realisateur) VALUES
(1, 'Christopher Nolan'),
(2, 'Quentin Tarantino'),
(3, 'James Cameron'),
(4, 'Greta Gerwig'),
(5, 'Steven Spielberg');

-- Ajout d'acteurs
INSERT INTO acteur (id, nom_acteur) VALUES
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
INSERT INTO boite_production (id, nom_boite_production) VALUES
(1, 'Warner Bros.'),
(2, 'Universal Pictures'),
(3, 'Paramount Pictures'),
(4, '20th Century Fox'),
(5, 'Sony Pictures');

-- Ajout de films
INSERT INTO film (id, nom_film, date_sortie, realisateur_id, boite_production_id, synopsis) VALUES
(1, 'Inception', '2010-07-16', 1, 1, 'Dom Cobb is a skilled thief who steals valuable secrets by infiltrating the subconscious of his targets while they dream.'),
(2, 'Pulp Fiction', '1994-10-14', 2, 2, 'The intertwined stories of several criminals in Los Angeles collide in unexpected ways.'),
(3, 'Titanic', '1997-12-19', 5, 4, 'The love story of Jack and Rose, two members of different social classes, aboard the legendary Titanic.'),
(4, 'La La Land', '2016-12-09', 4, 3, 'A love story between a passionate jazz musician and an aspiring actress in Los Angeles.'),
(5, 'The Matrix', '1999-03-31', 5, 1, 'A hacker named Neo discovers the truth about the simulated reality he lives in.'),
(6, 'Forrest Gump', '1994-07-06', 3, 2, 'The extraordinary story of Forrest Gump, a man with a low IQ, but who has witnessed significant historical moments in the United States.'),
(7, 'The Dark Knight', '2008-07-18', 1, 1, 'Batman faces the Joker, a psychotic criminal who seeks to create chaos in Gotham City.'),
(8, 'The Shawshank Redemption', '1994-09-10', 3, 4, 'The touching story of the friendship between two inmates sentenced to life at Shawshank prison.'),
(9, 'Inglourious Basterds', '2009-05-20', 2, 2, 'During World War II, a group of Jewish-American soldiers known as the Basterds targets Nazis.'),
(10, 'Avatar', '2009-12-18', 5, 4, 'On the moon Pandora, a paraplegic marine is sent on a diplomatic mission but gets involved in a conflict between humans and the Navi, an alien race.');

-- Associer des genres aux films
INSERT INTO film_genre (film_id, genre_id) VALUES
(6, 3), -- Forrest Gump (Drama)
(7, 1), -- The Dark Knight (Action)
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
