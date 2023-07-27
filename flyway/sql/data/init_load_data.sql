-- \copy crime_data(
--     type, 
--     year, 
--     month, 
--     day, 
--     hour, 
--     minute, 
--     hundred_block, 
--     neighbourhood, 
--     x, 
--     y) 
--     FROM 'crimedata_csv_all_years.csv' DELIMITER ',' CSV HEADER;

-- Create a temporary table with the same structure as the crime_data table
CREATE TEMP TABLE temp_crime_data (
    type VARCHAR(255),
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

\COPY temp_crime_data (type, year, month, day, hour, minute, hundred_block, neighbourhood, x, y) FROM 'crimedata_csv.csv' DELIMITER ',' CSV HEADER WHERE x::numeric <> 0 AND y::numeric <> 0;

TRUNCATE TABLE crime_data;

INSERT INTO crime_data ( type, year, month, day, hour, minute, hundred_block, neighbourhood, x, y) SELECT type, year, month, day, hour, minute, hundred_block, neighbourhood, x, y FROM temp_crime_data;

DROP TABLE temp_crime_data;
