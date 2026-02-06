import {useContext} from 'react';
import {Link, useNavigate} from 'react-router-dom';
import {AuthContext} from '../context/AuthContext';
import Button from './Button';
import logo from '../assets/logo.png';
import '../css/navbar.css'

/*Componente per centralizzare la barra di navigazione.
  Utilizza l'AuthContext per gestire la sessione e in particolare il logout.*/
export function Navbar() {
  
  const {logout} = useContext(AuthContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout(); 
    navigate('/login'); 
  };

  return (
    <nav className = "navbar">
      <div className = "navbar-center">
        <Link to = "/" className="navbar-home">          
          <img src={logo} alt="AgriEuro Logo" className="navbar-logo"/>
        </Link>
      </div>

      <div className = "navbar-right">
        <Button onClick={handleLogout} className="logout-button"> Logout</Button>
      </div>
    </nav>
  );
}