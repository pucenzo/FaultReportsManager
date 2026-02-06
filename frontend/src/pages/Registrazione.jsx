import InputField from '../components/InputField';
import Button from '../components/Button';
import {useState} from 'react';
import {useNavigate, Link} from 'react-router-dom';
import axios from 'axios';
import '../css/Registration.css'

/*Gestisce la registrazione del cliente. Passa un JSON che deve rispettare
  lo schema definito nel backend*/
function Registration() {
  const [nome, setNome] = useState("");
  const [cognome, setCognome] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (event) => {
    event.preventDefault(); 
    setError(''); 
    
    try {
      const userData = { 
        nome: nome,
        cognome: cognome,
        email : email,
        password : password,
      }; 
      await axios.post("http://localhost:8000/register", userData);
      navigate('/login');
    } catch (apiError) {
      if (apiError.response && apiError.response.data) { 
        const errorDetail = apiError.response.data.detail;
        const errorMessage = Array.isArray(errorDetail)?errorDetail[0].msg: errorDetail; 
        setError(errorMessage);
      } else {
        setError("Si è verificato un errore imprevisto. Riprova."); 
      }
    }
  };

  return (
    <div className = "registration-page">
      <h1 className = "form-title"> Crea un account </h1>

      <form onSubmit = {handleRegister} className = "registration-form">
        
        <InputField 
            type = "text" 
            placeholder = "Nome"
            className = "nome-field"
            required = {true}
            value={nome}
            onChange={(e) => setNome(e.target.value)}
        />

        <InputField 
            type = "text" 
            placeholder = "Cognome"
            className = "cognome-field"
            required = {true}
            value={cognome}
            onChange={(e) => setCognome(e.target.value)}
        />

        <InputField 
            type = "email" 
            placeholder = "Indirizzo email"
            className = "email-field"
            required = {true}
            value = {email}
            onChange = {(e) => setEmail(e.target.value)}
            iconName = "mail"          
          />

        <InputField 
            type = "password" 
            placeholder = "Password"
            className = "password-field"
            required = {true}
            value = {password}
            onChange = {(e) => setPassword(e.target.value)}
            iconName = "lock"
        />

        <Button 
            className = "registration-button"
            type = "submit">
            Crea un account
        </Button>

        <p className = "login-now"> Hai già un account? <Link to = "/login"> Accedi ora </Link></p>

        {error && <p style={{ color: 'red' }}>{error}</p>}
      
      </form>
    </div>
  );
}

export default Registration;