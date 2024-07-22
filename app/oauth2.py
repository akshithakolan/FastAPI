# from jose import JWTError, jwt
import jwt
from datetime import datetime, timedelta


#secret_key, algorithm hs-256, expiration time of the token

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    #provide the time -current to add 30min
    expire = datetime.now() + timedelta(minutes=(ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    #to create the jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
