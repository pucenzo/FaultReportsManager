import {useContext} from 'react';
import {Navigate} from 'react-router-dom';
import {AuthContext} from '../context/AuthContext';

/*Componente utilizzato per proteggere tutte le rotte che richiedono
  che l'utente sia loggato, quindi private. Lo reindirizza se non lo è*/
function ProtectedRoute({children}) {
  const {token} = useContext(AuthContext);

  if (!token) {
    return <Navigate to = "/login" replace />;
  }
  return children;
}

export default ProtectedRoute;