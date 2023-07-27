-- Create a composite index on the columns
CREATE INDEX idx_duplicate_identifiers ON crime_data (type, year, month, day, hour, minute, hundred_block, neighbourhood, x, y);
