import { useState, useContext } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom';
import InputField from '../components/InputField';
import Button from '../components/Button';
import { AuthContext } from '../context/AuthContext';
import '../css/Login.css'

/*Gestisce l'acquisizione delle credenziali e l'inizializzazione della sessione.*/
function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();
  const {login} = useContext(AuthContext);

  /*Gestisce l'invio dei dati di login secondo il formato OAuth2*/
  const handleLogin = async (event) => {
    event.preventDefault();
    setError(''); 

    try {
      const formData = new URLSearchParams(); 
      
      formData.append('username', email);
      formData.append('password', password); 


      const response = await axios.post("http://localhost:8000/login", formData);
      const token = response.data.access_token;
      await login(token);
        
      navigate('/');

    } catch (apiError) {
      if (apiError.response && apiError.response.data) { 
        setError(apiError.response.data.detail);
      } else {
        setError("Si è verificato un errore di connessione. Riprova.");  
      }
    }
  };

  return (
    <div className = "login-page">
      <h1 className = "form-title"> Accedi con </h1>

      <form onSubmit = {handleLogin} className = "login-form">
        <InputField 
          type = "email" 
          placeholder = "Indirizzo Email"
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
          onChange = {e => setPassword(e.target.value)}
          iconName = "lock"          
          />

        <Button 
            className = "login-button"
            type = "submit">
            Accedi
        </Button>

        <p className = "register-now"> Non hai un account? <Link to = "/registrazione"> Registrati ora </Link></p>

        {error && <p style={{ color: 'red' }}>{error}</p>}
      </form>
    </div>
  );
}

export default Login;