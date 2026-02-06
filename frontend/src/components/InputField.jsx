import { useState } from "react";

/*Componente campo di input, utilizzato per centralizzare le impostazioni di tutti i campi di input*/
function InputField({type, placeholder, className, iconName, required = false, value, onChange}) {
    const [isPasswordVisible, setIsPasswordVisible] = useState(false);
    
    return (
        <div className = "input-wrapper">
            <input 

                type = {isPasswordVisible && type === 'password' ? 'text' : type}
                placeholder = {placeholder} 
                className={`input-field ${className || ''}`}
                required = {required} 
                value = {value} 
                onChange = {onChange} 
            />
            <i className = "material-symbols-rounded">
                {iconName}
            </i> 
            {type === 'password' && (<i onClick = {() => setIsPasswordVisible(prevState => !prevState)} className = "eye-icon material-symbols-rounded">{isPasswordVisible ? 'visibility' : 'visibility_off'}</i>)}
        </div>
    );
}

export default InputField;