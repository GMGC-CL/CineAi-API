from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

#transforma o retorno dos objetos do banco de dados em json
def transform_to_json(movie:object):
    try:
        movie = dict(movie)
        return movie
    except Exception as e:
        print(e)
        return False
    
# api/controllers/auth_utils.py


# Chave secreta e algoritmo para o JWT
SECRET_KEY = "your_secret_key"  # Troque por uma chave secreta segura
ALGORITHM = "HS256"

# Inicialização do contexto do Passlib para criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=15)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
