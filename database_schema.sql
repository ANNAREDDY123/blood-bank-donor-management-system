CREATE TABLE users(
    id INTEGER PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255),
    role VARCHAR(30)
);

CREATE TABLE donors(
    id INTEGER PRIMARY KEY,
    name VARCHAR(100),
    age INTEGER,
    blood_group VARCHAR(10),
    phone VARCHAR(15) UNIQUE,
    city VARCHAR(100),
    last_donation_date DATE,
    is_eligible BOOLEAN
);

CREATE TABLE inventory(
    id INTEGER PRIMARY KEY,
    blood_group VARCHAR(10),
    units_available INTEGER,
    expiry_date DATE,
    storage_location VARCHAR(100)
);

CREATE TABLE requests(
    id INTEGER PRIMARY KEY,
    hospital_name VARCHAR(100),
    blood_group VARCHAR(10),
    units_required INTEGER,
    request_date DATE,
    status VARCHAR(30)
);
