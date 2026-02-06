from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.schemas import TokenData

"""configurazione dell'hashing della password"""
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""funzione di generazione di password hashate"""
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

"""funzione di verifica tra password in chiaro ed hashata """
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

"""algoritmo di firma crittografica"""
ALGORITHM = "HS256"

SECRET_KEY = settings.SECRET_KEY

"""funzione di codifica del token. Include nel token il soggetto, il ruolo, l'id e la durata"""
def create_access_token(soggetto: str, ruolo: str, id: int, expires_delta: timedelta) -> str: 
    expire = datetime.now(timezone.utc) + expires_delta

    """dati da codificare"""
    to_encode = {"sub": soggetto, "role": ruolo, "id": id, "exp": expire}

    """codifica del token comprensiva di firma del token con la chiave segreta e l'algoritmo"""
    encoded_jwt = jwt.encode( 
        to_encode, 
        settings.SECRET_KEY,
        algorithm=ALGORITHM
    ) 
    return encoded_jwt

"""funzione di decodifica del token e verifica di validità"""
def decode_access_token(token: str) -> TokenData|None:
    try:

        """decodifica del token con verifica della firma e della scadenza"""
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM])
        
        """spacchetta il token e verifica che rispetti il nostro schema"""
        token_data = TokenData(**payload)

        return token_data
    except JWTError:
        return None