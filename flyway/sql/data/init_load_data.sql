\copy crime_data(
    offence, 
    year, 
    month, 
    day, 
    hour, 
    minute, 
    hundred_block, 
    neighbourhood, 
    x, 
    y) 
    FROM 'crimedata_csv_all_years.csv' DELIMITER ',' CSV HEADER;