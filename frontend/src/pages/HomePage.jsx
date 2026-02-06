import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { DashboardCliente } from './DashboardCliente';
import { DashboardOperatore } from './DashboardOperatore';

/*smista l'utente alla propria dashboard a seconda del ruolo*/
function HomePage() {
  const {user, logout} = useContext(AuthContext);

  if (!user) { 
    return <div>Caricamento del profilo...</div>;
  }

  if (user.ruolo === 'cliente') { 
    return <DashboardCliente />; 
  } else if (user.ruolo === 'operatore') {
    return <DashboardOperatore />;
  }
}

export default HomePage;