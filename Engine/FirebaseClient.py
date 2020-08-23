import pyrebase
import time

def getFirebase():
    config = {
        "apiKey": "AIzaSyAYTc8g4A6AuWxEsZv8ETebkeiseS6sRVY",
        "authDomain": "cryptodata-ab1e2.firebaseapp.com",
        "databaseURL": "https://cryptodata-ab1e2.firebaseio.com",
        "projectId": "cryptodata-ab1e2",
        "storageBucket": "cryptodata-ab1e2.appspot.com",
        "messagingSenderId": "518294849950",
        "appId": "1:518294849950:web:7ef53f8bc67b110383ae8f"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db

def balance_update(sessionID, portfolio):
    db = getFirebase()
    timestamp= str(round(time.time()))
    portfolio = str(portfolio)
    data = {}
    data[timestamp] = portfolio
    results = db.child(str(sessionID)+"/portfolio").update(data)


def position_update(sessionID, position):
    db = getFirebase()
    timestamp= str(round(time.time()))
    position = str(position)
    data = {}
    data[timestamp] = position
    results = db.child(str(sessionID)+"/position").update(data)

def quote_update(sessionID, quote):
    db = getFirebase()
    timestamp= str(round(time.time()))
    quote = str(quote)
    data = {}
    data[timestamp] = quote
    results = db.child(str(sessionID)+"/price").update(data)
