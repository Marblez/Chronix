import pyrebase
import time
import Library

def getFirebase():
    config = {
        "apiKey": "AIzaSyACWoPHw74B89ZshAhezbKFGr9q0XWAPOw",
        "authDomain": "tach-1ff2f.firebaseapp.com",
        "databaseURL": "https://tach-1ff2f.firebaseio.com",
        "projectId": "tach-1ff2f",
        "storageBucket": "tach-1ff2f.appspot.com",
        "messagingSenderId": "954930106547",
        "appId": "1:954930106547:web:aaab9d293d55d41724e0c6"
    }

    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    return db

def update(name, value, balance, holdings, price, actions):
    db = getFirebase()
    name = name.replace("/","")
    timestamp = str(round(time.time()))
    data = {}
    data['Value'] = value
    data['Balance'] = balance
    data['Holdings'] = holdings
    data['Price'] = price
    db.child(name+"/"+str(timestamp)).update(data)
    if len(actions) > 0:
        for i in range(0, len(actions)):
            actions_list = {}
            curr_action = {}
            curr_action["Action"] = actions[i].action
            curr_action["Amount"] = actions[i].amount
            actions_list[i] = curr_action
        db.child(name+"/"+str(timestamp)+"/Actions").update(actions_list)
