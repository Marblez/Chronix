import pyrebase
import time
import Library

def getFirebase():
    config = {
        "apiKey": "AIzaSyAGQkImi9nWZiKPu9t_fGQywJCyRfjMsns",
        "authDomain": "naut-4cf9e.firebaseapp.com",
        "databaseURL": "https://naut-4cf9e.firebaseio.com",
        "projectId": "naut-4cf9e",
        "storageBucket": "naut-4cf9e.appspot.com", 
        "messagingSenderId": "81144661136", 
        "appId": "1:81144661136:web:c5122f3bef155ac7c78415" 
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db

def log(name, group, arr):
    db = getFirebase()
    for i in range(0, len(arr)):
        data = {}
        data[group] = arr[i]
        db.child(name + "/" + str(i)).update(data)

