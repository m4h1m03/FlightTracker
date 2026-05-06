"""
ETL pipeline for the OpenSky Network flight tracker.
Fetches a snapshot of all currently-airborne aircraft, then loads it into Postgres
across three tables: snapshots (one row per fetch), aircraft (deduplicated), 
and observations (one row per (aircraft, snapshot) pair).
"""

import psycopg 
from dotenv import load_dotenv
import os
import requests
import json
from datetime import datetime, timezone

load_dotenv()   # reads variables from .env file and sets them in the os.environ

# -- fetch live data from OpenSki --
response = requests.get('https://opensky-network.org/api/states/all')
response_dict = response.json()

# -- Build aircraft rows for bulk insert
flights = response_dict['states']
aircraft_rows = []
for flight in flights:
    aircraft = (flight[0], flight[2])
    aircraft_rows.append(aircraft)

with psycopg.connect(dbname=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), host= os.getenv('DB_HOST'), port=os.getenv('DB_PORT')) as conn:
    with conn.cursor() as cur:
        
        # -- loading snapshot into the database
        snapshot_time = datetime.fromtimestamp(response_dict['time'], tz=timezone.utc) # -- Use UTC so the value is unambiguous regardless of where the script runs --
        flight_count = len(flights)
        fetch_duration = 0
        fetch_status = 'success'
        cur.execute(
        'INSERT INTO snapshots (snapshot_time, flight_count, fetch_duration, fetch_status) VALUES (%s, %s, %s, %s) RETURNING id',
        (snapshot_time, flight_count, fetch_duration, fetch_status)
        )
        snapshot_id = cur.fetchone()[0]
        print(snapshot_id)

        # -- Same aircraft appears across many snapshots; skip if we've already recorded it
        cur.executemany(
        'INSERT INTO aircraft (icao24, origin_country) VALUES (%s, %s) ON CONFLICT (icao24) DO NOTHING',
         aircraft_rows
        )
       
            
        # cur.executemany(
        # 'INSERT INTO observations'
        # )

