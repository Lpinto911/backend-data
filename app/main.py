# Comentarios en español: backend-data consulta MongoDB por cédula
from fastapi import FastAPI, HTTPException
import os
from pymongo import MongoClient

app = FastAPI()

MONGO_HOST = os.getenv('MONGO_HOST','mongodb')
MONGO_PORT = int(os.getenv('MONGO_PORT','27017'))
MONGO_DB = os.getenv('MONGO_DB','commentsdb')

client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
db = client[MONGO_DB]
collection = db['people']

@app.get('/person/{cedula}')
def get_person(cedula: str):
    doc = collection.find_one({'cedula': cedula})
    if not doc:
        raise HTTPException(status_code=404, detail='Not found')
    return {'cedula': doc['cedula'], 'name': doc.get('name')}
