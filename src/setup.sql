-- schema

CREATE TABLE IF NOT EXISTS utenti(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    cognome TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    ruolo TEXT CHECK(ruolo IN('organizzatore','partecipante')) NOT NULL,
    data_registrazione TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS performances(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_artista TEXT UNIQUE NOT NULL,
    giorno TEXT CHECK(giorno IN('Venerdi','Sabato','Domenica')) NOT NULL,
    orario TEXT NOT NULL,
    durata INTEGER NOT NULL,
    descrizione TEXT NOT NULL,
    palco TEXT CHECK(palco IN('Palco A','Palco B','Palco C')) NOT NULL,
    genere TEXT NOT NULL,
    immagine BLOB,
    pubblicato INTEGER DEFAULT 0,
    id_organizzatore INTEGER NOT NULL,
    data_inserimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_organizzatore) REFERENCES utenti(id)
);

CREATE TABLE IF NOT EXISTS biglietti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_partecipante INTEGER UNIQUE NOT NULL,
    tipo TEXT CHECK(tipo IN ('Biglietto Giornaliero', 'Pass 2 Giorni', 'Full Pass')) NOT NULL,
    data_acquisto TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(id_partecipante) REFERENCES utenti(id)
);

CREATE TABLE IF NOT EXISTS biglietti_giorni (
    id_biglietto INTEGER NOT NULL,
    giorno TEXT CHECK(giorno IN ('Venerdi', 'Sabato', 'Domenica')) NOT NULL,
    PRIMARY KEY(id_biglietto, giorno),
    FOREIGN KEY(id_biglietto) REFERENCES biglietti(id)
);

-- dati

INSERT INTO utenti (nome, cognome, email, password, ruolo) VALUES
('Luna', 'Celeste', 'luna@aurora.com', 'organizzatore123', 'organizzatore'),
('Marco', 'Bosco', 'marco@aurora.com', 'organizzatore123', 'organizzatore'),
('Anna', 'Verdi', 'anna@gmail.com', 'partecipante123', 'partecipante'),
('Giorgio', 'Neri', 'giorgio@gmail.com', 'partecipante123', 'partecipante'),
('Elisa', 'Rossi', 'elisa@gmail.com', 'partecipante123', 'partecipante');

INSERT INTO performances (nome_artista, giorno, orario, durata, descrizione, palco, genere, pubblicato, id_organizzatore)
VALUES
-- Venerdì
('Solar Echoes', 'Venerdi', '18:00', 60, 'Un viaggio sonoro attraverso ambient e downtempo elettronico.', 'Palco A', 'Elettronica', 1, 1),
('The Wood Spirits', 'Venerdi', '19:15', 45, 'Folk acustico con strumenti tradizionali da tutto il mondo.', 'Palco B', 'World Music', 1, 1),
('Nocturna Loop', 'Venerdi', '20:30', 50, 'Live set techno dark su visuali oniriche.', 'Palco C', 'Techno', 1, 2),
('Mystic Flows', 'Venerdi', '21:45', 40, 'Jazz psichedelico in ambientazione multisensoriale.', 'Palco A', 'Jazz', 1, 2),
('Hidden Frequencies', 'Venerdi', '23:00', 60, 'Performance sperimentale binaurale.', 'Palco B', 'Sperimentale', 0, 1), -- non pubblicata
-- Sabato
('Echo Nomads', 'Sabato', '17:00', 60, 'Fusion tra sonorità mediorientali e synth analogici.', 'Palco A', 'Fusion', 1, 1),
('Lumen Sky', 'Sabato', '18:30', 45, 'Indie-pop con elementi elettronici ambient.', 'Palco B', 'Indie Pop', 1, 1),
('Drift Mechanics', 'Sabato', '19:45', 60, 'Drum & Bass atmosferico con video generativi.', 'Palco C', 'D&B', 1, 2),
('Aurora Collective', 'Sabato', '21:00', 50, 'Ensemble elettronico + strumenti dal vivo.', 'Palco A', 'Live Set', 1, 2),
('Nebula Bloom', 'Sabato', '22:30', 40, 'Trio vocale femminile in performance visiva.', 'Palco B', 'Vocal', 0, 1), -- non pubblicata
-- Domenica
('Raindrop Ritual', 'Domenica', '16:00', 45, 'Percussioni tribali e canto armonico.', 'Palco A', 'Tribal', 1, 1),
('Kaleido Waves', 'Domenica', '17:15', 50, 'Pop psichedelico in quadrofonia immersiva.', 'Palco B', 'Psy Pop', 1, 1),
('Analog Forest', 'Domenica', '18:30', 60, 'Composizioni ambient ispirate alla natura.', 'Palco C', 'Ambient', 1, 2),
('Digital Sorcery', 'Domenica', '20:00', 55, 'Set IDM con visuals ispirati al glitch art.', 'Palco A', 'IDM', 1, 2),
('The Final Echo', 'Domenica', '21:30', 60, 'Set collettivo con chiusura multisensoriale.', 'Palco B', 'Multigenere', 0, 1); -- non pubblicata

INSERT INTO biglietti (id_partecipante, tipo) VALUES
(3, 'Biglietto Giornaliero'),
(4, 'Pass 2 Giorni'),
(5, 'Full Pass');

-- un tipo di biglietto ciascuno

INSERT INTO biglietti_giorni (id_biglietto, giorno) VALUES
(1, 'Venerdi');

INSERT INTO biglietti_giorni (id_biglietto, giorno) VALUES
(2, 'Sabato'),
(2, 'Domenica');

INSERT INTO biglietti_giorni (id_biglietto, giorno) VALUES
(3, 'Venerdi'),
(3, 'Sabato'),
(3, 'Domenica');

