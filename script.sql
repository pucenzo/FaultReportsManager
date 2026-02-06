/* CREAZIONE TABELLE */

CREATE TABLE clienti(
    id INTEGER PRIMARY KEY,
    nome VARCHAR NOT NULL,
    cognome VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    hashed_pw VARCHAR NOT NULL
);

CREATE TABLE stati_segnalazione(
    id INTEGER PRIMARY KEY,
    nome VARCHAR NOT NULL UNIQUE
);

CREATE TABLE segnalazioni(
    id INTEGER PRIMARY KEY,
    titolo VARCHAR NOT NULL ,
    descrizione TEXT NOT NULL,
    priorita ENUM("Bassa", "Media", "Alta")  DEFAULT "Bassa",
    data_apertura TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operatore VARCHAR,

    id_cliente INTEGER,
    id_stato INTEGER,

    FOREIGN KEY(id_cliente) REFERENCES clienti(id),
    FOREIGN KEY(id_stato) REFERENCES stati_segnalazione(id)
);

CREATE TABLE operatori(
    id INTEGER PRIMARY KEY,
    nome VARCHAR NOT NULL,
    cognome VARCHAR NOT NULL,
    email VARCHAR NOT NULL UNIQUE,
    hashed_pw VARCHAR NOT NULL
);

CREATE TABLE log_stato_segnalazioni(
    id INTEGER PRIMARY KEY,
    vecchio_stato VARCHAR NOT NULL,
    nuovo_stato VARCHAR NOT NULL,
    data_modifica TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    operatore VARCHAR,

    id_segnalazione INTEGER,

    FOREIGN KEY(id_segnalazione) REFERENCES segnalazioni(id)
);

CREATE TABLE messaggi(
    id INTEGER PRIMARY KEY,
    contenuto TEXT NOT NULL,
    data_invio TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    autore VARCHAR NOT NULL,
    ruolo VARCHAR NOT NULL,

    id_segnalazione INTEGER,

    FOREIGN KEY (id_segnalazione) REFERENCES segnalazioni(id)
);

/* INIZIALIZZAZIONE STATI DB */

INSERT INTO stati_segnalazione(nome) VALUES(
    ("Aperta"),
    ("In Lavorazione"),
    ("Risolta"),
    ("Chiusa")
);

/* QUERY CRUD_CLIENTE */

INSERT INTO clienti(nome, cognome, email, hashed_pw) VALUES(
    "Elia", 
    "Cicio",
    "eliacicio@gmail.com",
    "$2b$12$q4sxxYtgAueT4VJam6.YTuoPtbwhAr3V3uiTcGdo/NNxrB3lyIR6."    
);

SELECT * FROM cliente WHERE email = "eliacicio@gmail.com";

/* QUERY CRUD_LOG */

INSERT INTO log_stato_segnalazioni(
    vecchio_stato, nuovo_stato, operatore, id_segnalazione
) VALUES (
    "Aperta", 
    "In Lavorazione",    
    "Operatore",
    "1"
)

SELECT * FROM log_stato_segnalazioni 
WHERE id_segnalazione  = 1 
ORDER BY data_modifica ASC

/* QUERY CRUD_OPERATORE */

INSERT INTO operatori(
    nome, 
    cognome, 
    email, 
    hashed_pw
) VALUES (
    "Elia", 
    "Admin", 
    "eliacicio@admin.com", 
    "$2b$12$FjKP8usp53LerBi50CEVEuCqmzmgwGOCqTaShVLNbYwXf.yfYKw6y"
)

SELECT * FROM operatori
WHERE email = "eliacicio@admin.com"

/* QUERY CRUD_SEGNALAZIONE */

INSERT INTO segnalazioni(
    titolo,
    descrizione,
    id_cliente,
    id_stato,
) VALUES (
    "titolo della segnalazione",
    "descrizione della segnalazione",
    "1"
    "1"
)

INSERT INTO messaggi(
    contenuto,
    autore,
    ruolo,
    id_segnalazione,
) VALUES (
    "Il contenuto del messaggio - descrizione",
    "Elia Cicio",
    "Cliente",
    "1"
)

SELECT 
    S.id AS id_segnalazione,
    S.titolo,
    S.descrizione,
    S.priorita,
    S.data_apertura,
    S.operatore
    
    ST.nome AS nome_stato,
    
    C.nome AS nome_cliente,
    C.cognome AS cognome_cliente, 
    C.email AS cognome_email,
    
    M.id AS id_messaggio,
    M.contenuto AS contenuto_messaggio,
    M.data_invio,
    M.autore AS autore_messaggio,

FROM segnalazioni S
JOIN clienti C ON S.id_cliente = C.id
JOIN stati_segnalazione ST ON S.id_stato = ST.id
LEFT JOIN messaggi M ON S.id = M.id_segnalazione
WHERE S.id = 1;

SELECT
    S.id AS id_segnalazione, 
    S.titolo,
    S.descrizione, 
    S.priorita,
    S.data_apertura,
    S.operatore

    C.nome AS nome_cliente,
    C.cognome
    c.email

    ST.nome AS nome_stato
FROM segnalazioni S
JOIN clienti C ON S.id_cliente = C.id
JOIN stati_segnalazione ST ON S.id_stato = ST.id
WHERE S.id = 1;

SELECT * FROM segnalazioni WHERE id_stato = 1

SELECT * FROM segnalazioni WHERE id_priorita = 1

SELECT
    S.id
    S.titolo,
    S.descrizione, 
    S.priorita,
    S.data_apertura,
    S.operatore

    C.nome AS nome_cliente,
    C.cognome AS cognome_cliente,
    c.email AS email_cliente,

    ST.nome AS nome_stato
FROM segnalazioni S
JOIN clienti C ON S.id_cliente = C.id
JOIN stati_segnalazione ST ON S.id_stato = ST.id
WHERE S.id_stato = 1 
AND S.id_priorita = "Bassa"

SELECT
    S.id
    S.titolo,
    S.descrizione, 
    S.priorita,
    S.data_apertura,
    S.operatore

    C.nome AS nome_cliente,
    C.cognome AS cognome_cliente,
    c.email AS email_cliente,

    ST.nome AS nome_stato
FROM segnalazioni S
JOIN clienti C ON S.id_cliente = C.id
JOIN stati_segnalazione ST ON S.id_stato = ST.id
WHERE S.id_cliente = 1
AND S.id_stato = 1 
AND S.id_priorita = "Bassa"

DELIMITER //
CREATE TRIGGER stato_update
AFTER UPDATE ON segnalazioni
FOR EACH ROW
BEGIN
    DECLARE nome_vecchio_stato VARCHAR;
    DECLARE nome_nuovo_stato VARCHAR;

    IF OLD.id_stato != NEW.id_stato THEN

        SELECT nome INTO nome_vecchio_stato FROM stati_segnalazione WHERE id = OLD.id_stato;
        SELECT nome INTO nome_nuovo_stato FROM stati_segnalazione WHERE id = NEW.id_stato;

        INSERT INTO logs_stato_segnalazioni 
        (vecchio_stato, nuovo_stato, operatore, id_segnalazione, data_modifica)
        VALUES 
        (nome_vecchio_stato, nome_nuovo_stato, NEW.operatore, NEW.id, NOW());
    END IF;
END //
DELIMITER ;

/* QUERY CRUD_STATO */

SELECT * FROM stati_segnalazioni WHERE nome = "Aperta"

SELECT * FROM stati_segnalazioni