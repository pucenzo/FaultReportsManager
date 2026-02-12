# FaultReportsManager

## Piattaforma di Segnalazioni

### Stack ed implementazione

La soluzione è stata implementata adottando lo stack:
 • fastAPI, con validazione dei dati tramite Pydantic, SQLAlchemy come ORM e SQLite come database in locale;
 • React, con gestione delle chiamate API tramite axios;
All'interno della repository è presente anche uno script SQL con la traduzione delle classi e delle query SQLAlchemy in istruzioni SQL standard.

### Prerequisiti

Assicurarsi di avere installato sul proprio computer:

1.  **Node.js** - [Scarica qui](https://nodejs.org/)
2.  **Python 3.8+** - [Scarica qui](https://www.python.org/)

---

### Installazione e Avvio

Il progetto è diviso in due cartelle principali. Aprire due terminali diversi per eseguirli contemporaneamente.

#### 1️⃣ Configurazione del Backend (Python)

Aprire il terminale nella cartella "backend":

1.  **Creare un ambiente virtuale**:
    ```
    python -m venv .venv
    ```

2.  **Attivare l'ambiente virtuale**:
    * *Windows:* ` .venv/Scripts/activate`
    * *Mac/Linux:* `source .venv/bin/activate`
    
3.  **Installare le dipendenze**:
    ```
    pip install -r requirements.txt
    ```

4. **Posizionarsi nella directory `backend`**:
    ```
    cd backend
    ```

5.  **Inizializzare il Database**:
    ```
    python -m app.init_db
    ```

6.  **Avviare il Server**:
    ```
    uvicorn main:app --reload
    ```
    Il backend sarà attivo all'indirizzo: `http://localhost:8000`

---

#### 2️⃣ Creazione utente Operatore

Mentre per i clienti la registrazione è autonoma mediante form, per gli operatori, essendo figure interne all'azienda, ho pensato di simulare il loro "accreditamento" tramite inserimento diretto nel database. Quindi non è prevista una pagina di registrazione pubblica per lo staff.

Per creare un nuovo operatore sarà necessario:

1. Aprire il terminale nella cartella `backend`;
2. Eseguire il modulo Python dedicato:
    ```
    python -m app.crea_operatore
    ```
3. Inserire i dati richiesti;

Una volta creato l'account, l'operatore potrà effettuare l'accesso dalla pagina di [login](http://localhost:5173/login).

#### 3️⃣ Configurazione del Frontend (React)

Aprire un nuovo terminale e andare nella cartella "frontend"":

1.  **Installare i pacchetti Node**:
    ```
    npm install
    ```

2.  **Avviare il sito**:
    ```
    npm run dev
    ```
    Il frontend sarà attivo all'indirizzo: `http://localhost:5173`

---

#### 4️⃣ Come testare l'App

1.  Andare alla pagina di registrazione all'indirizzo: (`http://localhost:5173/registrazione`);
2.  Creare un nuovo utente Cliente;
3.  Eseguire il login;
4.  Creare una nuova segnalazione dalla dashboard;
5.  Eseguire il logout;
6.  Eseguire il login come Operatore;
7.  Visualizzare nel dettaglio una segnalazione e testare le funzionalità (messaggio, cambio stato e priorita);
8.  Effettuare il logout e di nuovo il login come Cliente;
9.  Visualizzare nel dettaglio la segnalazione e tutte le modifiche/risposte apportate dall'Operatore;

---

#### Swagger UI - fastAPI

FastAPI genera automaticamente la documentazione, visualizzabile all'indirizzo `http://localhost:8000/docs`. 

Qui è possibile vedere e testare tutte le rotte direttamente dal browser.