CREATE TABLE IF NOT EXISTS raw_accidents (
    icr INT PRIMARY KEY,
    incident_type TEXT,
    incident_date TIMESTAMP,
    district TEXT,
    location_description TEXT,
    road_condition TEXT,
    vehicles_involved INT
);

CREATE TABLE IF NOT EXISTS raw_people (
    person_name TEXT,
    vehicle TEXT,
    residence TEXT,
    person_role TEXT,
    injury TEXT,
    helmet TEXT,
    seatbelt TEXT,
    alcohol TEXT,
    icr INT,
    gender TEXT,
    age INT,
    PRIMARY KEY(person_name, icr)
);

CREATE TABLE IF NOT EXISTS geo_accidents (
    icr INT PRIMARY KEY,
    incident_type TEXT,
    incident_date TIMESTAMP,
    district TEXT,
    location_description TEXT,
    road_condition TEXT,
    vehicles_involved INT,
    strd_location_description TEXT,
    x DOUBLE PRECISION,
    y DOUBLE PRECISION,
    geom GEOMETRY(POINT, 4326),
    city_id INT
);

CREATE TABLE IF NOT EXISTS ctu (
    id SERIAL PRIMARY KEY,
    ctu_name TEXT,
    class TEXT,
    county TEXT,
    pop INT,
    total_road_length DOUBLE PRECISION,
    aadt_sum DOUBLE PRECISION,
    aadt_mean DOUBLE PRECISION,
    geom GEOMETRY(GEOMETRY, 4326)
);

CREATE TABLE IF NOT EXISTS ctu_accidents (
    id SERIAL PRIMARY KEY,
    ctu_name TEXT,
    class TEXT,
    county TEXT,
    pop INT,
    total_road_length DOUBLE PRECISION,
    aadt_sum DOUBLE PRECISION,
    aadt_mean DOUBLE PRECISION,
    total_incident_count INT,
    predicted_count DOUBLE PRECISION,
    lmi_i DOUBLE PRECISION,
    lmi_q INT,
    lmi_p DOUBLE PRECISION,
    lmi_sig INT,
    lmi_label TEXT,
    geom GEOMETRY(GEOMETRY, 4326)
);
