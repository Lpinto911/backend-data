# Comentarios en español: backend-data consulta PostgreSQL por cédula
from fastapi import FastAPI, HTTPException
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

PG_HOST = os.getenv('POSTGRES_HOST', 'postgresql')
PG_PORT = int(os.getenv('POSTGRES_PORT', '5432'))
PG_DB = os.getenv('POSTGRES_DB', 'appdb')
PG_USER = os.getenv('POSTGRES_USER', 'postgres')
PG_PASS = os.getenv('POSTGRES_PASSWORD', '')

def get_conn():
    return psycopg2.connect(host=PG_HOST, port=PG_PORT, dbname=PG_DB, user=PG_USER, password=PG_PASS)

@app.get('/person/{cedula}')
def get_person(cedula: str):
    try:
        conn = get_conn()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT cedula, name FROM people WHERE cedula = %s', (cedula,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail='Not found')
        return {'cedula': row['cedula'], 'name': row.get('name')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
