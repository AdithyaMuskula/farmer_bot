from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# 🔐 Secret key (you can change later)
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080  # 7 days

# 🔒 Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ==============================
# HASH PASSWORD
# ==============================
def hash_password(password: str):
    return pwd_context.hash(password[:72])


# ==============================
# VERIFY PASSWORD
# ==============================
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password[:72], hashed_password)


# ==============================
# CREATE TOKEN
# ==============================
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# ==============================
# VERIFY TOKEN
# ==============================
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
    

# ==============================
# FASTAPI AUTH DEPENDENCY
# ==============================

# tells FastAPI where login endpoint is
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_token(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = payload.get("user_id")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id    