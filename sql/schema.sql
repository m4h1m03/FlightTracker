CREATE TABLE IF NOT EXISTS aircraft (
    icao24 TEXT PRIMARY KEY,
    origin_country TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS snapshots (
    id BIGSERIAL PRIMARY KEY,
    snapshot_time TIMESTAMPTZ NOT NULL,
    flight_count INTEGER NOT NULL,
    fetch_duration INTEGER NOT NULL,
    fetch_status TEXT NOT NULL DEFAULT 'success'
);

CREATE TABLE IF NOT EXISTS observations (
    icao24 TEXT NOT NULL,
    snapshot_id BIGINT NOT NULL,
    true_track DOUBLE PRECISION,
    time_position TIMESTAMPTZ,
    callsign TEXT,
    baro_altitude DOUBLE PRECISION,
    on_ground BOOLEAN NOT NULL,
    geo_altitude DOUBLE PRECISION,
    velocity DOUBLE PRECISION,
    vertical_rate DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    latitude DOUBLE PRECISION,
    last_contact TIMESTAMPTZ NOT NULL,
    position_source SMALLINT NOT NULL,
    sensors INTEGER[],
    squawk TEXT,
    spi BOOLEAN NOT NULL,
    PRIMARY KEY (icao24, snapshot_id),
    FOREIGN KEY (icao24) REFERENCES aircraft(icao24),
    FOREIGN KEY (snapshot_id) REFERENCES snapshots(id)
);