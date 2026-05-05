## Entities

# Can be split into 3 entities:

- Aircraft
- Snapshots
- Observations

Three tables chosen over two-table design to prevent repeating snapshot_time across every observation record which makes batch-level metadata (errors, counts, durations) easy to add later, and avoids update/insert/delete anomalies around snapshot events.

aircraft:
- icao24 (PK) TEXT NOT NULL HEX STRING
- origin_country TEXT NOT NULL 


snapshots:
- id, BIGSERIAL (PK)
- snapshot_time TIMESTAMPTZ NOT NULL
- flight_count INTEGER NOT NULL
- fetch_duration INTEGER NOT NULL
- fetch_status TEXT NOT NULL DEFAULT 'success'

observations:
- icao24 TEXT NOT NULL  -- FK to aircraft.icao24
- snapshot_id BIGINT NOT NULL  -- FK to snapshots.id
  PRIMARY KEY (icao24, snapshot_id)   -- composite
- true_track DOUBLE PRECISION
- time_position TIMESTAMPTZ 
- callsign TEXT 
- baro_altitude DOUBLE PRECISION
- on_ground BOOLEAN NOT NULL
- geo_altitude DOUBLE PRECISION
- velocity DOUBLE PRECISION
- vertical_rate DOUBLE PRECISION
- longitude DOUBLE PRECISION
- latitude DOUBLE PRECISION
- last_contact TIMESTAMPTZ NOT NULL 
- position_source SMALLINT NOT NULL
- sensors INTEGER[] 
- squawk TEXT
- spi BOOLEAN NOT NULL

 
 ## The relationships

 observations.icao24 references aircraft.icao24 (FK), (One aircraft has multiple observations)
 observations.snapshot_id reference snapshots.id (FK➡️) (One snapshot has multiple observations)

 Create the tables in the following order:

 1. aircraft (no dependancies)
 2. snapshots (no dependancies)
 3. observations (references both)
