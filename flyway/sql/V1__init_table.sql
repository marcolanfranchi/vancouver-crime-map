-- Create a new table to store crime data
CREATE TABLE crime_data (
    offence VARCHAR(255),
    year INT,
    month INT,
    day INT,
    hour INT,
    minute INT,
    hundred_block VARCHAR(255),
    neighbourhood VARCHAR(255),
    x FLOAT,
    y FLOAT
);
