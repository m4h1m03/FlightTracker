import psycopg
from dotenv import load_dotenv
import os

load_dotenv()   # reads variables from .env file and sets them in the os.environ

with psycopg.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), host= os.getenv('DB_HOST'), port=os.getenv('DB_PORT')) as conn:
    with conn.cursor() as cur:
        cur.execute(
        'INSERT INTO aircraft (icao24, origin_country) VALUES (%s, %s)',
        ('abcd12', 'TestCountry')
        )
    
