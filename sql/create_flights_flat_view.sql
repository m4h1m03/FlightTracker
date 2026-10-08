-- View used by the Looker Studio dashboard.
-- Flattens observations, snapshots and aircraft into one row per observation.
-- Note: snapshots.flight_count is a per-snapshot total repeated on every row,
-- so use record count (not SUM/AVG of flight_count) when counting aircraft.
CREATE OR REPLACE VIEW flights_flat AS
SELECT aircraft.icao24,
       observations.true_track,
       observations.time_position,
       observations.callsign,
       observations.baro_altitude,
       observations.on_ground,
       observations.geo_altitude,
       observations.velocity,
       observations.vertical_rate,
       observations.longitude,
       observations.latitude,
       observations.last_contact,
       observations.squawk,
       observations.spi,
       snapshots.snapshot_time,
       snapshots.flight_count,
       snapshots.fetch_duration,
       aircraft.origin_country
FROM observations
JOIN snapshots ON observations.snapshot_id = snapshots.id
JOIN aircraft ON observations.icao24 = aircraft.icao24;
