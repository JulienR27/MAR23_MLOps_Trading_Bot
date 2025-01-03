from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
from pandas import DataFrame
from csv import DictWriter
from joblib import load
import sys, os
from pathlib import Path
current_path = Path(os.getcwd())
project_path = current_path.parent.parent.as_posix()
sys.path.append(project_path)
from src.domain.utils.prediction import make_prediction

os.environ["PATH_TO_DATABASE"] = "users_db.csv"

api = FastAPI(
   title="Trading Bot API",
   description="Trading recommendation",
   version="1.0.0"
)

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependencies

def get_db():
    users_db = pd.read_csv(os.environ["PATH_TO_DATABASE"])
    return users_db

def get_current_user(credentials: HTTPBasicCredentials = Depends(security), users_db: DataFrame = Depends(get_db)):
    username = credentials.username
    #users_db = pd.read_csv("users_db.csv")

    if (username not in list(users_db["username"])) or not (pwd_context.verify(credentials.password, pwd_context.hash(users_db[users_db["username"]==username]["password"].iloc[0]))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return users_db[users_db["username"]==username]["right"].iloc[0]

def get_admin(credentials: HTTPBasicCredentials = Depends(security), users_db: DataFrame = Depends(get_db)):
    username = credentials.username
    #users_db = pd.read_csv("users_db.csv")

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

# Utils
def get_users(users_db: DataFrame):
    list_of_user_dicts = users_db.to_dict(orient='records')
    for user in list_of_user_dicts:
        user.pop("password")
    return list_of_user_dicts

# welcome
@api.get('/', name='Check if working', tags=['Use'])
def greetings(right: str = Depends(get_current_user)):
   return {"Welcome": f"Hello, you have {right} rights"}


# L'admin peut voir la liste des utilisateurs et leurs droits
class User(BaseModel):
    username: str
    password: str
    right: str

@api.get('/admin', name='Get all the users and their right', tags=['Admin'])
def get_users_endpoint(username: str = Depends(get_admin), users_db: DataFrame = Depends(get_db)):
    #users_db = pd.read_csv("users_db.csv")
    return get_users(users_db)


# L'admin peut rajouter des utilisateurs dans la BDD (A voir pour la gestion du mot de passe)
def create_user(user: User, right: str):
   # Dictionary that we want to add to csv database
   new_user_dict = user.dict()
   # list of column names
   field_names = list(new_user_dict.keys())
   # Opening CSV file in append mode and creating a file object for this file
   with open(os.environ["PATH_TO_DATABASE"], 'a') as f_object:
      # we pass the file object and the list of column names to DictWriter()
      dictwriter_object = DictWriter(f_object, fieldnames=field_names)
      # we pass the dictionary as an argument to the Writerow()
      dictwriter_object.writerow(new_user_dict)
      # we close the file object
      f_object.close()

@api.put('/admin', name='Add user to the database', tags=['Admin'])
def create_user_endpoint(user: User, right: str = Depends(get_admin)):
    create_user(user, right)
    return {"Status": "User added to the database"}


# L'admin peut modifier les droits des utilisateurs dans la BDD (A voir pour la gestion du mot de passe)
class UserRight(BaseModel):
    username: str
    right: str
    
@api.post('/admin', name='Modify user right in the database', tags=['Admin'])
def post_right(user: UserRight, right: str = Depends(get_admin)):
    users_db = pd.read_csv("users_db.csv")
    users_db.loc[users_db["username"]==user.username, "right"] = user.right
    users_db.to_csv('users_db.csv', index=False)
    return {"Status": "User right modified in the database"} 


# L'admin peut retirer des utilisateurs dans la BDD
def remove_user(user: UserRight, right: str):
    users_db = pd.read_csv(os.environ["PATH_TO_DATABASE"])
    new_users_db = users_db[users_db["username"] != user.username]
    new_users_db.to_csv(os.environ["PATH_TO_DATABASE"], index=False)

@api.delete('/admin', name='Remove user from the database', tags=['Admin'])
def remove_endpoint(user: UserRight, right: str = Depends(get_admin)):
    remove_user(user, right)
    return {"Status": "User removed from the database"} 

# L'utilisateur demande une prédiction sur le prix d'une ou plusieurs actions en donnant ses "Params"
possible_trading_type = ['market', 'fundamental', 'market_and_fundamental']
possible_horizon = ["1d", "1w", "2w", "1m"]

class Params(BaseModel):
   tickers: List[str]
   time_horizon: str 
   trading_type: str 

@api.post('/predictions', name="Get predictions according to params", tags=['Use'])
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
    # try:   
    # Making the predictions
    predictions = make_prediction(model, sector_encoder, params.time_horizon, params.trading_type, params.tickers)
    
    for ticker in predictions:
        predictions[ticker] = f"{round(predictions[ticker] * 100, 3)}%"
    
    return predictions

    # except ValueError:
    #   raise HTTPException(status_code=404, detail='You may have exceeded the requests limit')


# L'utilisateur demande une prédiction sur tout l'univers d'investissment en donnant ses "ParamsBest"
class ParamsBest(BaseModel):
   time_horizon: str 
   trading_type: str 
   
@api.post('/best', name="Get best stocks in environment", tags=['Use'])
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
