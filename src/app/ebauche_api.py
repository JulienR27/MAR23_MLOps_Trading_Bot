from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional, List, Union
import pandas as pd
from csv import DictWriter

api = FastAPI(
   title="Trading Bot API",
   description="Trading recommendation",
   version="1.0.0"
)

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_db = pd.read_csv("users_db.csv")

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if (username not in users_db) or not(pwd_context.verify(credentials.password, users_db[username])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def get_admin(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if (username != "admin"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not admin",
            headers={"WWW-Authenticate": "Basic"},
        ) 
    if not(pwd_context.verify(credentials.password, users_db[username])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# welcome
@api.get('/', name='Check if working')
def greetings(username: str = Depends(get_current_user)):
   return {"Welcome": f"Hello {username}"}


# L'admin peut voir la liste des utilisateurs et leurs droits
class User(BaseModel):
    username: str
    password: str
    right: str

@api.get('/admin', name='')
def get_users(user: User, username: str = Depends(get_admin)):
   return {"Users": "List of users and their rights"}   


# L'admin peut rajouter des utilisateurs dans la BDD" (A voir pour la gestion du mot de passe)
@api.put('/admin', name='')
def put_users(user: User, username: str = Depends(get_admin)):
   # Dictionary that we want to add to csv database
   users_dict = users_db.do_dict(orient='records')
   # list of column names
   field_names = list(users_dict.keys())
   # Opening CSV file in append mode and creating a file object for this file
   with open('users_db.csv', 'a') as f_object:
      # we pass the file object and the list of column names to DictWriter()
      dictwriter_object = DictWriter(f_object, fieldnames=field_names)
      # we pass the dictionary as an argument to the Writerow()
      dictwriter_object.writerow(question_dict)
      # we close the file object
      f_object.close()

   return #users added 


# L'admin peut rajouter des droits aux utilisateurs dans la BDD (A voir pour la gestion du mot de passe)
@api.post('/admin', name='')
def post_users(username: str = Depends(get_admin)):
   return #user right added   


# L'utilisateur demande une prédiction sur le prix d'une ou plusieurs actions en donnant ses "Params"
possible_trading_type = ['market', 'fundamental', 'market and fundamental']
possible_horizon = ["1d", "1w", "2w", "1m"]

class Params(BaseModel):
   ticker: List[str]
   trading_type: str 
   horizon: str 

@api.get('/predictions', name="Get predictions according to params")
def get_predictions(params: Params, username: str = Depends(get_current_user)):
   '''
   Generate predictions according to params
   '''
   if params.trading_type not in possible_trading_type:
      raise HTTPException(status_code=400, detail='Wrong trading type')

    if params.horizon not in possible_horizon:
      raise HTTPException(status_code=400, detail='Not a valid horizon')
    
   try:
        # Choosing the right model according to params
        # Making the predictions
      return #predictions
    
   except ValueError:
      raise HTTPException(status_code=404, detail='')

