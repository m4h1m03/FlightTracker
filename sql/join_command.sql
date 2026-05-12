
SELECT
aircraft.icao24,
true_track,
time_position,
callsign,
baro_altitude,
on_ground,
geo_altitude,
velocity,
vertical_rate,
longitude,
latitude,
last_contact,
squawk,
spi,
snapshot_time,
flight_count,
fetch_duration,
origin_country


FROM observations
JOIN snapshots ON observations.snapshot_id = snapshots.id
JOIN aircraft ON observations.icao24 = aircraft.icao24;