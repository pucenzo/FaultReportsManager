import { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { AuthContext } from '../context/AuthContext';
import Button from '../components/Button';
import '../css/DettaglioSegnalazione.css'; 

/*gestisce la vista dettaglio della segnalazione, compresa la chat e il cambio stato e priorita per l'operatore*/
export default function DettaglioSegnalazione() {
  
  const {id} = useParams();
  const {user, logout} = useContext(AuthContext);   
  const navigate = useNavigate();
  const [segnalazioneDettagli, setSegnalazioneDettagli] = useState(null);
  const [nuovoMessaggio, setNuovoMessaggio] = useState("");
  const [pageError, setPageError] = useState("");
  const [msgError, setMsgError] = useState("");
  const isOperatore = user?.ruolo === "operatore" 
  

  /*Carica i dettagli della segnalazione*/
  const fetchDettagli = async () => {
    try {
      const response = await axios.get(`http://localhost:8000/segnalazioni/${id}`);
      setSegnalazioneDettagli(response.data);
    } catch (apiError) {
      if (apiError.response && apiError.response.status === 401) {
            logout(); 
            return;
        } 
      console.error(apiError);
      setPageError("Errore nel caricamento della segnalazione.");
    } 
  };

  /*ricarica i dettagli ogni volta che cambia l'id della segnalazione e il token*/
  useEffect(() => {
    if (user) {
        fetchDettagli();
    }
  }, [id, user]);

  /*gestisce l'invio del messaggio ricaricando la pagina dei dettagli all'invio*/
  const handleInviaMessaggio = async (e) => {
    e.preventDefault();
    setMsgError("");

    try {
      await axios.post(`http://localhost:8000/segnalazioni/${id}/messaggi`,{ contenuto: nuovoMessaggio });
      setNuovoMessaggio("");
      await fetchDettagli(); 
    } catch (apiError) {
      if (apiError.response && apiError.response.status === 401) {
            logout();
            return;
      }
      if (apiError.response && apiError.response.data) { 
        const errorDetail = apiError.response.data.detail; 
        if (Array.isArray(errorDetail)) {
          setMsgError(errorDetail[0].msg); 
        } else {
          setMsgError(errorDetail); 
        }
      } else { 
        setMsgError("Errore nell'invio del messaggio");
      }
    }
  };

  /*gestisce il cambio dello stato, inviando il messaggio e ricaricando i dettagli*/
  const handleCambiaStato = async (nuovoIdStato) => {
    try {
      await axios.put(`http://localhost:8000/segnalazioni/${id}/aggiorna_stato`,{id_stato: parseInt(nuovoIdStato)});
      fetchDettagli(); 
    } catch (apiError) {
      if (apiError.response && apiError.response.status === 401) {
            logout();
            return;
      } 
      alert("Errore aggiornamento stato.");
    }
  };

  /*gestisce il cambio della priorita, inviando il messaggio e ricaricando i dettagli*/
  const handleCambiaPriorita = async (nuovaPriorita) => {
    try {
      await axios.put(`http://localhost:8000/segnalazioni/${id}/aggiorna_priorita`,{priorita: nuovaPriorita});
      fetchDettagli();
    } catch (apiError) {
      if (apiError.response && apiError.response.status === 401) {
            logout();
            return;
      } 
      alert("Errore aggiornamento priorità.");
    }
  };

  if (pageError) return <div className="error-msg" style={{color:"red"}}>{pageError}</div>;
  if (!segnalazioneDettagli) return <div className="error-msg">Segnalazione non trovata.</div>;

  /*formatta la data per mostrarla in formato gg-mm-aaaa*/
  const formattaData = (dataString) => {
    if (!dataString) return "-";

    const dataDaConvertire = dataString.endsWith("Z") ? dataString : dataString + "Z";
    const data = new Date(dataDaConvertire);

    return data.toLocaleString('it-IT', {
      timeZone: 'Europe/Rome',
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="dettaglio-container">      
      <div className={`main-content ${!isOperatore ? 'full-width' : ''}`}>        
        <div className="segnalazione-header">
            <button onClick={() => navigate('/')} className="indietro-button">
                <span className="material-symbols-rounded">arrow_back</span> Torna alla lista
            </button>

          {!isOperatore && (
             <div className="indicatore-stato-priorita">
                Stato: <strong>{segnalazioneDettagli.stato.nome}</strong> | Priorità: <strong>{segnalazioneDettagli.priorita}</strong>
             </div>
          )}
        </div>

        <div className="lista-messaggi">
          <div className="header-messaggi">
            <div className="colonna-data">Data</div>
            <div className="colonna-autore">Autore</div>
            <div className="colonna-messaggio">Messaggio</div>
          </div>

          {segnalazioneDettagli.messaggi && segnalazioneDettagli.messaggi.map((messaggio) => (
            <div key={messaggio.id} className="riga-messaggio">
              <div className="data-messaggio">
                {formattaData(messaggio.data_invio)}
              </div>
              <div className="autore-messaggio">
                <strong>{messaggio.autore}</strong>
              </div>
              <div className="contenuto-messaggio">
                {messaggio.descrizione}
                {messaggio.contenuto}
              </div>
            </div>
          ))}
        </div>

        <div className="input-messaggio">
          <form onSubmit={handleInviaMessaggio}>
            <textarea 
              placeholder="Scrivi un messaggio..."
              className = "box-messaggio"
              required = {true} 
              value={nuovoMessaggio}
              onChange={(e) => setNuovoMessaggio(e.target.value)}
              rows="3"
            />
            {msgError && <div className="error-msg" style={{color: "red"}}>{msgError}</div>}                                
            <div className="bottone-invio">
                <Button type="submit">Invia Messaggio</Button>
            </div>
          </form>
        </div>
      </div>

      {isOperatore && (
        <div className="barra-laterale">
            <h3>Gestione Ticket</h3>
            
            <div className="gestione-stato">
            <label>Stato</label>
            <select 
                value={segnalazioneDettagli.stato.id} 
                onChange={(e) => handleCambiaStato(e.target.value)}
                className="selezione-stato"
            >
                <option value="1">Aperta</option>
                <option value="2">In Lavorazione</option>
                <option value="3">Risolta</option>
                <option value="4">Chiusa</option>
            </select>
            </div>

            <div className="gestione-priorita">
            <label>Priorità</label>
            <select 
                value={segnalazioneDettagli.priorita}
                onChange={(e) => handleCambiaPriorita(e.target.value)}
                className="selezione-priorita"
            >
                <option value="Bassa">Bassa</option>
                <option value="Media">Media</option>
                <option value="Alta">Alta</option>
            </select>
            </div>            
        </div>
      )}

    </div>
  );
}