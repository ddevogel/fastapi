import logging
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from jwt import ExpiredSignatureError
from passlib.context import CryptContext

from .views import Token, TokenData, User, UserInDB

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_ISSUER = "org.org"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

fake_users_db = {
    "johndoe": {
        "id": "c3eaab46-fa77-4274-8631-8b2b6b609d38",
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$oRDZSPtYoJsIhxUg10GLNO7i7cZwwf9e5Ew.5/E/xNEu2.HP8BGYi",
        "disabled": False,
        "scopes": ["artist_read"],
    }
}


async def get_current_user(
    request: Request,
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme),
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        nickname: str = payload.get("nickname")
        if nickname is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(sub=sub, scopes=token_scopes, nickname=nickname)
    except (JWTError, ExpiredSignatureError,) as e:
        logging.error(f'Token="{token}" - {e}')
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.nickname)
    if user is None:
        raise credentials_exception
    request.state.current_user = user
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    request.state.current_user = user


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def build_access_token(user: UserInDB) -> Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = encode_access_token(
        data={
            "sub": user.id,
            "nickname": user.username,
            "scopes": user.scopes,
            "iss": ACCESS_TOKEN_ISSUER,
        },
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


def encode_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
