import { Outlet } from 'react-router-dom';
import { Navbar } from './Navbar';

/*Componente per centralizzare il layout di tutte le pagine
  Permette di avere la navbar montata per tutte le pagine*/
function AppLayout() {
  return (
    <div>
      <Navbar />
      <main>
        <Outlet />
      </main>
    </div>
  );
}

export default AppLayout;