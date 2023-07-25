from src.app.main import get_users, create_user, remove_user
from pydantic import BaseModel
import pandas as pd
import os

os.environ["PATH_TO_DATABASE"] = "test_users_db.csv"

class User(BaseModel):
    username: str
    password: str
    right: str

class UserRight(BaseModel):
    username: str
    right: str

def test_get_users():
    test_users_db = pd.read_csv(os.environ["PATH_TO_DATABASE"])
    test_users = get_users(test_users_db)
    assert test_users[0]["username"] == "test"
    assert test_users[0]["right"] == "tester"

# from csv import DictWriter
# def create_user(user: User, right: str):
#    # Dictionary that we want to add to csv database
#    new_user_dict = user.dict()
#    # list of column names
#    field_names = list(new_user_dict.keys())
#    # Opening CSV file in append mode and creating a file object for this file
#    with open(os.environ["PATH_TO_DATABASE"], 'a') as f_object:
#       # we pass the file object and the list of column names to DictWriter()
#       dictwriter_object = DictWriter(f_object, fieldnames=field_names)
#       # we pass the dictionary as an argument to the Writerow()
#       dictwriter_object.writerow(new_user_dict)
#       # we close the file object
#       f_object.close()

def test_create_user():
    old_test_users_db = pd.read_csv(os.environ["PATH_TO_DATABASE"])
    nb_rows_old = old_test_users_db.shape[0]
    print(nb_rows_old)
    user = User(username="test_create", password="test_create_password", right="tester")
    create_user(user=user, right="admin")
    new_test_users_db = pd.read_csv(os.environ["PATH_TO_DATABASE"])
    nb_rows_new = new_test_users_db.shape[0]
    print(nb_rows_new)
    assert nb_rows_new == nb_rows_old + 1 
    assert new_test_users_db.loc[new_test_users_db["username"]=="test_create", "password"].values[0] == "test_create_password"

def test_remove_user():
    old_test_users_db = pd.read_csv(os.environ["PATH_TO_DATABASE"])
    nb_rows_old = old_test_users_db.shape[0]
    print(nb_rows_old)
    user = UserRight(username="test_create", right="tester")
    remove_user(user=user, right="admin")
    new_test_users_db = pd.read_csv(os.environ["PATH_TO_DATABASE"])
    nb_rows_new = new_test_users_db.shape[0]
    print(nb_rows_new)
    assert nb_rows_new == nb_rows_old - 1 
    assert new_test_users_db[new_test_users_db["username"]=="test_create"].empty
