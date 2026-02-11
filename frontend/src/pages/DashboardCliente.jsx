import {useState, useEffect, use, useContext} from 'react';
import {useNavigate} from 'react-router-dom';
import axios from 'axios';
import '../css/Dashboard.css';
import Button from '../components/Button';
import InputField from '../components/InputField';
import {AuthContext} from '../context/AuthContext';

export function DashboardCliente() {

  const [showForm, setShowForm] = useState(false);
  const[segnalazioni, setSegnalazioni] = useState([]);
  const[error, setError] = useState("");
  const [formError, setFormError] = useState('');
  const [titolo, setTitolo] = useState('');
  const [descrizione, setDescrizione] = useState('');
  const [filtroPriorita, setFiltroPriorita] = useState("");
  const [filtroStato, setFiltroStato] = useState("");
  const [activeDropdown, setActiveDropdown] = useState(null);
  const nomiStati = {"1": "Aperta","2": "In Lav.", "3": "Risolta","4": "Chiusa"};
  const navigate = useNavigate();
  const {logout} = useContext(AuthContext);

  /*Gestisce la vista principale del cliente,
    dal caricamento dei dati, alla creazione della segnalazione,
    ai filtri fino alla visualizzazione*/
  const fetchSegnalazioniCliente = async () => {
      try{
        const params = {};
        if (filtroPriorita) params.priorita = filtroPriorita;
        if (filtroStato) params.id_stato = filtroStato;
        const response = await axios.get("http://localhost:8000/segnalazioni", {params});
        setSegnalazioni(response.data);
      } catch (error){
        if (error.response && error.response.status === 401) {
            logout(); 
            return;
        }         
        setError("Impossibile recuperare le segnalazioni.");
        console.error("Errore durante il recupero delle segnalazioni:", error);
      }
    };

  /*Ricarica la visualizzazione del cliente ogni volta che cambia la priorita e lo stato*/
  useEffect(() => {    
    fetchSegnalazioniCliente();
  }, [filtroPriorita, filtroStato]);
  
  /*gestore della creazione delle segnalazioni*/
  const handleCreaSegnalazione = async (event) =>{

    event.preventDefault();
    setFormError('');

    const dati = {
      titolo: titolo,
      descrizione: descrizione
    }

    try{
      await axios.post("http://localhost:8000/segnalazioni/", dati);
      fetchSegnalazioniCliente();
      
      setTitolo(''); 
      setDescrizione('');
      setShowForm(false);
    } catch (apiError) { 
      if (apiError.response && apiError.response.status === 401) {
        setError("Sessione scaduta. Effettua nuovamente il login.");
        logout(); 
        return;
      } 
      if (apiError.response && apiError.response.data) { 
        const errorDetail = apiError.response.data.detail; 
        if (Array.isArray(errorDetail)) {
            setFormError(errorDetail[0].msg); 
        } else {
            setFormError(errorDetail); 
        }
      } else {
        setFormError("Errore nella creazione della segnalazione."); 
      }
    }
  };

  /*gestisce l'apertura del menu a tendina*/
  const toggleDropdown = (menuName) => {
    setActiveDropdown(activeDropdown === menuName ? null : menuName);
  };

  /*gestisce la selezione dei filtri per stato e priorità*/
  const handleFilterSelect = (type, value) => {
    if (type === 'stato') setFiltroStato(value);
    if (type === 'priorita') setFiltroPriorita(value);
    setActiveDropdown(null); 
  };

  return (
    <div className="dashboard-container cliente-css">    
    
        <div className="table-container">
          
          <div className="header-tabella">
            <div className="colonna-icona"></div>
            <div className="colonna-stato">
              <div 
                  className={`header-clickable ${filtroStato ? "filter-active" : ""}`} 
                  onClick={() => toggleDropdown('stato')}
              >
                  {filtroStato ? nomiStati[filtroStato] : "Stato"}
                  
                  <i className="material-symbols-rounded header-arrow">
                      keyboard_arrow_down
                  </i>
              </div>

              {activeDropdown === 'stato' && (
                  <div className="dropdown-menu">
                      <div className="dropdown-reset" onClick={() => handleFilterSelect('stato', '')}>
                          Tutti (Reset)
                      </div>
                      <div className="dropdown-stato" onClick={() => handleFilterSelect('stato', '1')}>
                          Stato: Aperta
                      </div>
                      <div className="dropdown-stato" onClick={() => handleFilterSelect('stato', '2')}>
                          Stato: In Lavorazione
                      </div>
                      <div className="dropdown-stato" onClick={() => handleFilterSelect('stato', '3')}>
                          Stato: Risolta
                      </div>
                      <div className="dropdown-stato" onClick={() => handleFilterSelect('stato', '4')}>
                          Stato: Chiusa
                      </div>
                  </div>
              )}
            </div>

            <div className="colonna-priorita">
                <div 
                    className={`header-clickable ${filtroPriorita ? "filter-active" : ""}`} 
                    onClick={() => toggleDropdown('priorita')}
                >
                    {filtroPriorita ? filtroPriorita : "Priorità"}

                    <i className="material-symbols-rounded header-arrow">
                        keyboard_arrow_down
                    </i>
                </div>

                {activeDropdown === 'priorita' && (
                    <div className="dropdown-menu">
                        <div className="dropdown-reset" onClick={() => handleFilterSelect('priorita', '')}>
                            Tutte (Reset)
                        </div>
                        <div className="dropdown-priorita" onClick={() => handleFilterSelect('priorita', 'Bassa')}>
                            Bassa
                        </div>
                        <div className="dropdown-priorita" onClick={() => handleFilterSelect('priorita', 'Media')}>
                            Media
                        </div>
                        <div className="dropdown-priorita" onClick={() => handleFilterSelect('priorita', 'Alta')}>
                            Alta
                        </div>
                    </div>
                )}
            </div>
            <div className="colonna-titolo">Titolo</div>
            <div className="colonna-operatore">Operatore</div>
            <div className="colonna-data">Data Creazione</div>
          </div>

          <div className="tabella-segnalazioni">
            {segnalazioni.length === 0 ? (
              <p className="messaggio-vuoto">Nessuna segnalazione trovata.</p>
            ) : (
              segnalazioni.map((segnalazione) => (
                <div key={segnalazione.id} className="riga-tabella">                  
                  <div className="colonna-icona">
                    <i 
                      className="material-symbols-rounded action-icon"
                      onClick={() => navigate(`/segnalazioni/${segnalazione.id}`)}
                      style={{ cursor: "pointer" }}
                    >
                      visibility
                    </i>
                  </div>
                  <div className="colonna-stato"> <span className={`stato`}> {segnalazione.stato.nome} </span> </div>
                  <div className="colonna-priorita"> {segnalazione.priorita} </div>
                  <div className="colonna-titolo"> {segnalazione.titolo} </div>
                  <div className="colonna-operatore"> {segnalazione.operatore ? segnalazione.operatore : "-"} </div>
                  <div className="colonna-data"> {new Date(segnalazione.data_apertura).toLocaleDateString('it-IT')} </div>
                </div>
              ))
            )}
          </div>
        </div>

        <div className="crea-segnalazione-container">
          {!showForm && (
            <Button className="bottone-crea-segnalazione" onClick={() => setShowForm(true)}>
              Crea Segnalazione
            </Button>
          )}

          {showForm && (
            <div className="form-creazione-container">
              <h2 style={{marginTop: 0}}>Compila i campi della segnalazione</h2>          
              <form className = "form-crea-segnalazione" onSubmit={handleCreaSegnalazione}>
                <div>              
                  <InputField 
                    type="text"
                    placeholder="Titolo della segnalazione"
                    className="titolo"
                    required = {true}
                    value={titolo} 
                    onChange={(e) => setTitolo(e.target.value)}
                  />
                </div>

                <div>
                  <textarea
                    className="descrizione" 
                    placeholder="Descrivi il problema"
                    required={true}                    
                    rows="4" 
                    value={descrizione}
                    onChange={(e) => setDescrizione(e.target.value)}
                  />
                  {formError && <div className="error-msg" style={{color: "red"}}>{formError}</div>}                                
                </div>

                <div className="form-button">
                  <Button type="submit" className="invia-segnalazione">Invia Segnalazione</Button>
                  <Button 
                    type="button" 
                    className="annulla-segnalazione"
                    onClick={() => { 
                      setShowForm(false); 
                      setFormError(""); 
                      setTitolo('');
                      setDescrizione('');
                    }}
                  >
                    Annulla
                  </Button>
                </div>
              </form>
            </div>
      )}
        </div>
        {error && <div className="messaggio-errore" style={{color: "red"}}>{error}</div>}
    </div>
  );
}