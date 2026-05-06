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
from datetime import datetime, timezone

load_dotenv()   # reads variables from .env file and sets them in the os.environ

# -- fetch live data from OpenSky --
response = requests.get('https://opensky-network.org/api/states/all')
response_dict = response.json()

# -- Build aircraft rows for bulk insert --
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
        (snapshot_time, flight_count, fetch_duration, fetch_status))
        snapshot_id = cur.fetchone()[0]
        print(snapshot_id)

        # -- Same aircraft appears across many snapshots; skip if we've already recorded it
        cur.executemany(
        'INSERT INTO aircraft (icao24, origin_country) VALUES (%s, %s) ON CONFLICT (icao24) DO NOTHING',
         aircraft_rows
        )
        # -- Build observation rows for bulk insert --
        observation_rows = []
        for flight in flights:
            observation = (snapshot_id, flight[0], None if flight[1] is None else flight[1].strip(), None if flight[3] is None else datetime.fromtimestamp(flight[3], tz=timezone.utc), datetime.fromtimestamp(flight[4], tz=timezone.utc) , flight[5], flight[6], flight[7], flight[8], flight[9], flight[10], flight[11], flight[12], flight[13], flight[14], flight[15], flight[16])
            observation_rows.append(observation)    

        cur.executemany('''
        INSERT INTO observations (
        snapshot_id, 
        icao24,
        callsign, 
        time_position,
        last_contact,
        longitude,
        latitude,
        baro_altitude,
        on_ground,
        velocity,
        true_track,
        vertical_rate,
        sensors,
        geo_altitude,
        squawk,
        spi,
        position_source
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
        observation_rows                
        )

