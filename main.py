from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta  
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from sqlalchemy import Integer, create_engine, Table, MetaData, Column, String, DateTime
import logging


SECRET_KEY = "aaafd44178fc0deff7e496e3d03df69e4265a08e65cfc592b11116188c92650b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


db = {
    "admin": {
        "username": "admin",
        "full_name": "Admin User",
        "email": "admin@gmail.com",
        "hashed_password": "$2b$12$Hh3nZnAYoghoEvKjMexwieh0om0a9OsH8dKHjWLkWfjJ9S9uPlsoK",
        "disabled": False,
    },
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str or None = None

class User(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None
    disabled: bool or None = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


engine = create_engine('sqlite:///mydatabase.db')
metadata = MetaData()
logins = Table('logins', metadata,
            Column('id', Integer, primary_key=True),
            Column('username', String),
            Column('login_time', DateTime)
)


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    try:
        connection = engine.connect()
        connection.execute(logins.insert().values(username=user.username, login_time=datetime.now()))
        connection.commit()  # Explicitly commit the transaction
        connection.close()
        logging.info("Login recorded in database for user: %s", user.username)
    except Exception as e:
        logging.error("Error inserting login record: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/logins/")
async def read_logins():
    try:
        with engine.connect() as connection:
            result = connection.execute(logins.select())
            # Assuming 'username' is the first column and 'login_time' is the second
            logins_list = [{'id': row[0], 'username': row[1], 'login_time': row[2]} for row in result]
            return logins_list
    except Exception as e:
        logging.error("Error fetching logins: %s", str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")

