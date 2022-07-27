import json
from flask import Flask
import socket
from pymongo import MongoClient

app = Flask(__name__)



def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017, 
                         username='root', 
                         password='pass',
                        authSource="admin")
    db = client["film"]
    return db

# Function to display hostname and IP address
def get_Host_name_IP():
    try:
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)
        print("Hostname :  ",host_name)
        print("IP : ",host_ip)
        return host_name, host_ip
    except:
        print("Unable to get Hostname and IP")


@app.route("/index", methods=["GET"])
def index():
        host, ip = get_Host_name_IP()
        return f'Up and runnning !!! IN => {host} , AT ADDRESS => {ip} '


@app.route('/insert')
def insert():
    try:
        js = json.load(open('Film.json','r'))
        print(js)
        film_db = get_db()
        film_coll= film_db["films"]
        film_coll.insert_many(js)
        return "Success"
    except Exception as e:
        print(str(e))
        return str(e)



@app.route('/get')
def get():
    film_db = get_db()
    film_coll= film_db["films"]
    result = list(film_coll.find({},{"_id":0}))
    return {"data":result}

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5000, debug = True) 