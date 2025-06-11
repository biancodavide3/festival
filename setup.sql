-- Schema

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
    immagine TEXT NOT NULL,
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

-- dati (la password per ogni utente e' "password")

INSERT INTO utenti (nome, cognome, email, password, ruolo) VALUES
('Andrea', 'Bianchi', 'andrea@gmail.com', 'scrypt:32768:8:1$JfuxD9WFwpX33phC$53a19f7b55a866cb760c4fe6dd58752c21f236182cc4118d61bd8b0abd563d76b10c792dcda0f1a700a5a13bec620ccf4b0e959f863f89fcdd503d0a8001be9d', 'organizzatore'),
('Marco', 'Bosco', 'marco@gmail.com', 'scrypt:32768:8:1$JfuxD9WFwpX33phC$53a19f7b55a866cb760c4fe6dd58752c21f236182cc4118d61bd8b0abd563d76b10c792dcda0f1a700a5a13bec620ccf4b0e959f863f89fcdd503d0a8001be9d', 'organizzatore'),
('Anna', 'Verdi', 'anna@gmail.com', 'scrypt:32768:8:1$JfuxD9WFwpX33phC$53a19f7b55a866cb760c4fe6dd58752c21f236182cc4118d61bd8b0abd563d76b10c792dcda0f1a700a5a13bec620ccf4b0e959f863f89fcdd503d0a8001be9d', 'partecipante'),
('Giorgio', 'Neri', 'giorgio@gmail.com', 'scrypt:32768:8:1$JfuxD9WFwpX33phC$53a19f7b55a866cb760c4fe6dd58752c21f236182cc4118d61bd8b0abd563d76b10c792dcda0f1a700a5a13bec620ccf4b0e959f863f89fcdd503d0a8001be9d', 'partecipante'),
('Elisa', 'Rossi', 'elisa@gmail.com', 'scrypt:32768:8:1$JfuxD9WFwpX33phC$53a19f7b55a866cb760c4fe6dd58752c21f236182cc4118d61bd8b0abd563d76b10c792dcda0f1a700a5a13bec620ccf4b0e959f863f89fcdd503d0a8001be9d', 'partecipante');

INSERT INTO performances (nome_artista, giorno, orario, durata, descrizione, palco, genere, immagine, pubblicato, id_organizzatore)
VALUES
-- Venerdì
('Solar Echoes', 'Venerdi', '18:00', 60, 'Energia pura e riff potenti in una performance rock coinvolgente.', 'Palco A', 'Rock', '/static/images/uploaded/4a1e9b25-9f3c-4ea5-a7b2-b2d68f453b91.jpg', 1, 1),
('The Wood Spirits', 'Venerdi', '19:15', 45, 'Rock energico con melodie accattivanti e testi appassionanti.', 'Palco B', 'Rock', '/static/images/uploaded/fd1a3e92-6c90-44e2-88b6-080b09e66c98.jpg', 1, 1),
('Nocturna Loop', 'Venerdi', '20:30', 50, 'Pop moderno con influenze dance e arrangiamenti freschi.', 'Palco C', 'Pop', '/static/images/uploaded/0f2b2e93-5c18-4a2e-8e61-0150982c12c4.jpg', 1, 2),
('Mystic Flows', 'Venerdi', '21:45', 40, 'Il massimo della musica elettronica.', 'Palco A', 'Electronic', '/static/images/uploaded/2e4c8cb1-0e0e-4b9a-9c6f-3a22f3c64f2d.jpg', 1, 2),
('Hidden Frequencies', 'Venerdi', '23:00', 60, 'Rock alternativo con un sound fresco e originale.', 'Palco B', 'Rock', '/static/images/uploaded/a92f27d3-25cb-41f3-9e75-85e17a14ac08.jpg', 0, 1),

-- Sabato
('Echo Nomads', 'Sabato', '17:00', 60, 'Brani potenti e coinvolgenti che fanno battere il cuore.', 'Palco A', 'Rock', '/static/images/uploaded/719f4c01-b394-40b1-b1ef-31d0e8cb29f9.jpg', 1, 1),
('Lumen Sky', 'Sabato', '18:30', 45, 'Indie-pop con elementi elettronici ambient.', 'Palco B', 'Pop', '/static/images/uploaded/6b4c1a5a-2bb9-4f1e-a2c2-cf39cb8c46cd.jpg', 1, 1),
('Drift Mechanics', 'Sabato', '19:45', 60, 'Armonia degli strumenti allo stato puro', 'Palco C', 'Classica', '/static/images/uploaded/89134b82-41e7-4552-bfaa-fb687261f4ee.jpg', 1, 2),
('Aurora Collective', 'Sabato', '21:00', 50, 'Una scarica di energia con chitarre distorte e ritmi serrati.', 'Palco A', 'Rock', '/static/images/uploaded/dfb1d95d-d590-4e0c-a8ec-0a631fbcc89c.jpg', 1, 2),
('Nebula Bloom', 'Sabato', '22:30', 40, 'Trio vocale femminile in performance visiva.', 'Palco B', 'Pop', '/static/images/uploaded/3e80cf79-1c64-4045-9d99-fbe05843f9cd.jpg', 0, 1),

-- Domenica
('Raindrop Ritual', 'Domenica', '16:00', 45, 'Una band capace di far vibrare ogni palco con il loro rock autentico.', 'Palco A', 'Rock', '/static/images/uploaded/efc5ea0d-195f-4e35-bb76-2c119d1c60e1.jpg', 1, 1),
('Kaleido Waves', 'Domenica', '17:15', 50, 'Rock psichedelico da brividi.', 'Palco B', 'Rock', '/static/images/uploaded/cc2c4b6f-90f7-45d0-81e0-d650e1901e47.jpg', 1, 1),
('Analog Forest', 'Domenica', '18:30', 60, 'Composizione Rock ispirata alla natura.', 'Palco C', 'Rock', '/static/images/uploaded/90a924f9-3f7d-4cf0-a01c-c7e384bf99cd.jpg', 1, 2),
('Digital Sorcery', 'Domenica', '20:00', 55, 'Pop fresco che unisce ballate emotive e brani uptempo.', 'Palco A', 'Pop', '/static/images/uploaded/ce2b2a06-2cbf-4f3b-b07d-f73a5bfe30d4.jpg', 1, 2),
('The Final Echo', 'Domenica', '21:30', 60, 'Sound pulito e produzioni curate per un pop irresistibile.', 'Palco B', 'Pop', '/static/images/uploaded/ae16a19b-fd8d-4d13-b1f2-9a80e42e02a1.jpg', 0, 1);


INSERT INTO biglietti (id_partecipante, tipo) VALUES
(3, 'Biglietto Giornaliero'),
(4, 'Pass 2 Giorni'),
(5, 'Full Pass');

-- Un tipo di biglietto ciascuno

INSERT INTO biglietti_giorni (id_biglietto, giorno) VALUES
(1, 'Venerdi');

INSERT INTO biglietti_giorni (id_biglietto, giorno) VALUES
(2, 'Sabato'),
(2, 'Domenica');

INSERT INTO biglietti_giorni (id_biglietto, giorno) VALUES
(3, 'Venerdi'),
(3, 'Sabato'),
(3, 'Domenica');

