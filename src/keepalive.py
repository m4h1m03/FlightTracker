"""keepalive.py - daily ping so the Supabase free project doesn't pause."""


import os
import sys
import psycopg
from dotenv import load_dotenv
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(ENV_PATH)

REQUIRED = ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]


def get_settings():
    missing = []
    settings = {}
    for name in REQUIRED:
        value = os.getenv(name)
        if value is None or value == '':
            missing.append(name)
        else:
            settings[name] = value
    if len(missing) != 0:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")
    return settings


def ping(settings):
    with psycopg.connect(
        host=settings['DB_HOST'], 
        port=settings['DB_PORT'], 
        dbname=settings['DB_NAME'], 
        user=settings['DB_USER'], 
        password=settings['DB_PASSWORD']
    ) as conn:
    
        with conn.cursor() as cur:
            cur.execute('''
                SELECT COUNT(*)
                FROM aircraft
                '''
            )
            count = cur.fetchone()[0]
    return count
    


def main():
    settings = get_settings()
    count = ping(settings)
    print(f'keepalive OK, count: {count}')


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Keepalive failed: {exc}", file=sys.stderr)
        sys.exit(1)
