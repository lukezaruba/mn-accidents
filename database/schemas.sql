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
    geom GEOMETRY(POINT, 4326)
);