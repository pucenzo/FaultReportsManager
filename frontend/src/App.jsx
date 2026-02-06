import {Routes, Route} from 'react-router-dom';
import Login from "./pages/Login";
import HomePage from "./pages/HomePage";
import Registration from "./pages/Registrazione";
import Layout from './components/Layout';
import DettaglioSegnalazione from './pages/DettaglioSegnalazione';
import ProtectedRoute from './components/ProtectedRoute';
import {DashboardCliente} from './pages/DashboardCliente';
import {DashboardOperatore} from './pages/DashboardOperatore';

/*Definisce le rotte dell'app e ne protegge alcune con l'autenticazione*/
function App() {  
  return (
    <div className = "app-container">

      <Routes>
        <Route path="/login" element={<div className = "login-container"> <Login /> </div>} />
        <Route path="/registrazione" element={<div className = "registration-container"> <Registration /> </div>} />

        <Route element = {<ProtectedRoute> <Layout/> </ProtectedRoute>}>
          <Route path = "/" element = {<ProtectedRoute> <HomePage /> </ProtectedRoute>} />
          <Route path= "/segnalazioni/:id" element={<ProtectedRoute> <DettaglioSegnalazione /> </ProtectedRoute>} />
          <Route path= "/" element={<ProtectedRoute> <DashboardOperatore /> </ProtectedRoute>} />
          <Route path= "/" element={<ProtectedRoute> <DashboardCliente /> </ProtectedRoute>} />
        </Route>
      </Routes>
    </div>
  );
}

export default App;