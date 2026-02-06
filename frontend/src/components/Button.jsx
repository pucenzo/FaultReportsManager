/*Componente bottone, utilizzato per centralizzare lo stile e il comportamento di tutti i bottoni*/
function Button({className, type, children, onClick}) {
    return (
        <button 
            className = {className} 
            type = {type}
            onClick={onClick} 
        >            
            {children}
        </button>
    );
}

export default Button;