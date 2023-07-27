-- Add the datetime column
ALTER TABLE crime_data
ADD COLUMN datetime TIMESTAMP;

-- Update the datetime column based on the existing columns
UPDATE crime_data
SET datetime = TO_TIMESTAMP(CONCAT(year, '-', month, '-', day, ' ', hour, ':', minute), 'YYYY-MM-DD HH24:MI');
