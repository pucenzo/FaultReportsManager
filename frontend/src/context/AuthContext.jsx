import { createContext, useState, useEffect, useCallback } from 'react';
import axios from 'axios';

/*Contesto di autenticazione globale. Permette di accedere a utente e token
  ovunque, in ogni componente*/
const AuthContext = createContext();

function AuthProvider({children}) {

  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  /*Carica i dati dell'utente tramite l'endpoint user/me*/
  const fetchUserData = useCallback(async () => {

    const currentToken = localStorage.getItem('token');

    if (currentToken) {
      try {
        axios.defaults.headers.common['Authorization'] = `Bearer ${currentToken}`;
        const response = await axios.get('http://localhost:8000/user/me');
        setUser(response.data); 
        return response.data; 
      } catch (error) {  
        console.error("Token non valido, logout in corso:", error); 
        logout();
        return null; 
      }
    } else { 
      delete axios.defaults.headers.common['Authorization'];
      setUser(null);
      return null;
    }
  }, []);

  /*Ogni volta che cambia il token reidentifichiamo l'utente*/
  useEffect(() => {
    fetchUserData();
  }, [token, fetchUserData]);

  /*effettua il login caricando il token nel localStorage del browse e nello stator*/
  const login = async (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken); 
    return await fetchUserData(); 
  };

  /*effettua il logout eliminando il token dal localStorage del broser e dallo stato*/
  const logout = () => {
    localStorage.removeItem('token'); 
    setToken(null); 
    setUser(null);
    delete axios.defaults.headers.common['Authorization'];
  };

  /*Impacchettiamo tutto ciò che vogliamo rendere pubblico*/
  const value = {
    token, 
    user, 
    login, 
    logout, 
    refetchUser: fetchUserData, 
  };

  /*Avvolge l'intera app e rende disponibile value a qualsiasi componente avvolto*/
  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export {AuthContext, AuthProvider};