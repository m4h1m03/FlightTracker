"""
ETL pipeline for the OpenSky Network flight tracker.
Fetches a snapshot of all currently-airborne aircraft, then loads it into Postgres
across three tables: snapshots (one row per fetch), aircraft (deduplicated), 
and observations (one row per (aircraft, snapshot) pair).
"""
import os
from pathlib import Path
from datetime import datetime, timezone
import time 
import sys
import logging

import psycopg 
from dotenv import load_dotenv
import requests

ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(ENV_PATH)   # reads variables from .env file and sets them in the os.environ

OPENSKY_URL = 'https://opensky-network.org/api/states/all'

logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')

# Helper functions for observation bulk insert used later
def clean_text(value):
    return None if value is None else value.strip()

def unix_to_utc(value):
    return None if value is None else datetime.fromtimestamp(value, tz=timezone.utc)

class FlightFetcher:
    def __init__(self, URL):
        self.URL = URL
    
    def fetch(self):
        # -- fetch live data from OpenSky --
        start = time.time()  # used for fetch _duration
        response = requests.get(self.URL)
        if response.status_code != 200:
            logging.error(f'OpenSky returned a {response.status_code}; aborting')
            sys.exit(1) 
        response_dict = response.json()
        flights = response_dict['states']
        fetch_duration = int((time.time() - start) * 1000) # milliseconds
        return response_dict, flights, fetch_duration

def main():
    
    fetcher = FlightFetcher(OPENSKY_URL)
    response_dict, flights, fetch_duration = fetcher.fetch()

    # -- Build aircraft rows for bulk insert --
    aircraft_rows = [(flight[0], flight[2]) for flight in flights] # Using (icao24, origin_country) tuple

    with psycopg.connect(
        dbname=os.getenv('DB_NAME'), 
        user=os.getenv('DB_USER'), 
        host=os.getenv('DB_HOST'), 
        port=os.getenv('DB_PORT')
    ) as conn:
        with conn.cursor() as cur:
    
            # -- loading snapshot into the database
            snapshot_time = datetime.fromtimestamp(response_dict['time'], tz=timezone.utc) # -- Use UTC so the value is unambiguous regardless of where the script runs --
            flight_count = len(flights)
            fetch_status = 'success'
            cur.execute(
            '''INSERT INTO snapshots (
            snapshot_time, flight_count, 
            fetch_duration, fetch_status
            ) VALUES (%s, %s, %s, %s) RETURNING id''',
            (snapshot_time, flight_count, fetch_duration, fetch_status))
            snapshot_id = cur.fetchone()[0]
            logging.info(f'snapshot {snapshot_id}, inserted {flight_count} flights at {snapshot_time} (took {fetch_duration}ms)')

            # -- Same aircraft appears across many snapshots; skip if we've already recorded it
            cur.executemany(
            'INSERT INTO aircraft (icao24, origin_country) VALUES (%s, %s) ON CONFLICT (icao24) DO NOTHING',
            aircraft_rows
            )
            # -- Build observation rows for bulk insert --
            
            observation_rows = []
            for flight in flights:
                icao, callsign, _, time_position, last_contact, longitude, latitude, baro_altitude, on_ground, velocity, true_track, vertical_rate, sensors, geo_altitude, squawk, spi, position_source = flight
                observation = (
                    snapshot_id, 
                    icao, 
                    clean_text(callsign), 
                    unix_to_utc(time_position), 
                    unix_to_utc(last_contact), 
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
                    )
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

if __name__ == "__main__":
    main()