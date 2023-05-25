from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
from csv import DictWriter
from joblib import load
import sys, os
from pathlib import Path
current_path = Path(os.getcwd())
project_path = current_path.parent.parent.as_posix()
sys.path.append(project_path)
from src.domain.utils.prediction import make_prediction


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
    if (username not in list(users_db["username"])) or not (pwd_context.verify(credentials.password, pwd_context.hash(users_db[users_db["username"]==username]["password"].iloc[0]))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return users_db[users_db["username"]==username]["right"].iloc[0]

def get_admin(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if users_db[(users_db["username"]==username) & (users_db["right"]=="admin")].any().sum() == 0:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You are not admin",
            headers={"WWW-Authenticate": "Basic"},
        ) 
    if not(pwd_context.verify(credentials.password, pwd_context.hash(users_db[users_db["username"]==username]["password"].iloc[0]))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return users_db[users_db["username"]==username]["right"].iloc[0]

# welcome
@api.get('/', name='Check if working')
def greetings(right: str = Depends(get_current_user)):
   return {"Welcome": f"Hello, you have {right} rights"}


# L'admin peut voir la liste des utilisateurs et leurs droits
class User(BaseModel):
    username: str
    password: str
    right: str

@api.get('/admin', name='Get all the users and their right')
def get_users(username: str = Depends(get_admin)):
    list_of_user_dicts = users_db.to_dict(orient='records')
    for user in list_of_user_dicts:
        user.pop("password")
    return list_of_user_dicts


# L'admin peut rajouter des utilisateurs dans la BDD (A voir pour la gestion du mot de passe)
@api.put('/admin', name='Add user to the database')
def put_users(user: User, right: str = Depends(get_admin)):
   # Dictionary that we want to add to csv database
   new_user_dict = user.dict()
   # list of column names
   field_names = list(new_user_dict.keys())
   # Opening CSV file in append mode and creating a file object for this file
   with open('users_db.csv', 'a') as f_object:
      # we pass the file object and the list of column names to DictWriter()
      dictwriter_object = DictWriter(f_object, fieldnames=field_names)
      # we pass the dictionary as an argument to the Writerow()
      dictwriter_object.writerow(new_user_dict)
      # we close the file object
      f_object.close()

   return {"Status": "User added to the database"}


# L'admin peut rajouter des droits aux utilisateurs dans la BDD (A voir pour la gestion du mot de passe)
class UserRight(BaseModel):
    username: str
    right: str
    
@api.post('/admin', name='Modify user right in the database')
def post_right(user: UserRight, right: str = Depends(get_admin)):
    users_db.loc[users_db["username"]==user.username, "right"] = user.right
    users_db.to_csv('users_db.csv', index=False)
    return {"Status": "User right modified in the database"} 


# L'admin peut retirer des utilisateurs dans la BDD
@api.delete('/admin', name='Remove user from the database')
def remove(user: UserRight, right: str = Depends(get_admin)):
    new_users_db = users_db[users_db["username"] != user.username]
    new_users_db.to_csv('users_db.csv', index=False)
    return {"Status": "User removed from the database"} 

# L'utilisateur demande une prédiction sur le prix d'une ou plusieurs actions en donnant ses "Params"
possible_trading_type = ['market', 'fundamental', 'market_and_fundamental']
possible_horizon = ["1d", "1w", "2w", "1m"]

class Params(BaseModel):
   tickers: List[str]
   time_horizon: str 
   trading_type: str 

@api.post('/predictions', name="Get predictions according to params")
def predict(params: Params, right: str = Depends(get_current_user)):
    '''
    Generate predictions according to params
    '''
    if params.trading_type not in possible_trading_type:
      raise HTTPException(status_code=400, detail='Wrong trading type')
    
    if right != "admin":
        if params.trading_type != right:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="You do not have corresponding rights",
                headers={"WWW-Authenticate": "Basic"})
            
    if params.time_horizon not in possible_horizon:
      raise HTTPException(status_code=400, detail='Not a valid horizon')
    
  
    # Loading the right model
    model = load(f'{project_path}/src/domain/trained_models/lgbm_{params.trading_type}_{params.time_horizon}.joblib') 
    # Loading sector encoder
    sector_encoder = load(f'{project_path}/src/domain/trained_models/label_encoder.joblib') 
    try:   
       # Making the predictions
        predictions = make_prediction(model, sector_encoder, params.time_horizon, params.trading_type, params.tickers)
        
        for ticker in predictions:
            predictions[ticker] = f"{round(predictions[ticker] * 100, 3)}%"
        
        return predictions
    
    except ValueError:
      raise HTTPException(status_code=404, detail='You may have exceeded the requests limit')


# L'utilisateur demande une prédiction sur tout l'univers d'investissment en donnant ses "ParamsBest"
class ParamsBest(BaseModel):
   time_horizon: str 
   trading_type: str 
   
@api.post('/best', name="Get best stocks in environment")
def predict_best_stocks(params: ParamsBest, right: str = Depends(get_current_user)):
   '''
   Generate predictions on entire stocks environment according to params
   '''
   if params.trading_type not in possible_trading_type:
     raise HTTPException(status_code=400, detail='Wrong trading type')
     
   if right != "admin":
       if params.trading_type != right:
           raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail="You do not have corresponding rights")  

   if params.time_horizon not in possible_horizon:
     raise HTTPException(status_code=400, detail='Not a valid horizon')
   
 
   # Loading the right model
   model = load(f'{project_path}/src/domain/trained_models/lgbm_{params.trading_type}_{params.time_horizon}.joblib') 
   # Loading sector encoder
   sector_encoder = load(f'{project_path}/src/domain/trained_models/label_encoder.joblib') 
   try:   
       # Making the predictions
       predictions = make_prediction(model, sector_encoder, params.time_horizon, params.trading_type)
        
       for ticker in predictions:
           predictions[ticker] = f"{round(predictions[ticker] * 100, 3)}%"
            
       return predictions
   
   except ValueError:
      raise HTTPException(status_code=404, detail='You may have exceeded the requests limit')
