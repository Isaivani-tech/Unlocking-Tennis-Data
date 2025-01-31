SELECT * FROM categories
SELECT * FROM competitions
SELECT * FROM complexes
SELECT * FROM venues
SELECT * FROM competitors
SELECT * FROM competitor_rankings

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'categories';

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'competitions';

-- 1. Modify the Categories Table
-- Change the data types and set constraints
ALTER TABLE categories
    ALTER COLUMN category_id SET DATA TYPE VARCHAR(50),
    ALTER COLUMN category_name SET DATA TYPE VARCHAR(100);

-- Set category_id as PRIMARY KEY
ALTER TABLE categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (category_id);

-- 2. Modify the Competitions Table
-- Change the data types and set constraints, including the 'level' column
ALTER TABLE competitions
    ALTER COLUMN competition_id SET DATA TYPE VARCHAR(50),
    ALTER COLUMN competition_name SET DATA TYPE VARCHAR(100),
    ALTER COLUMN parent_id SET DATA TYPE VARCHAR(50),
    ALTER COLUMN type SET DATA TYPE VARCHAR(20),
    ALTER COLUMN gender SET DATA TYPE VARCHAR(10),
    ALTER COLUMN category_id SET DATA TYPE VARCHAR(50),
    ALTER COLUMN level SET DATA TYPE VARCHAR(50);  -- Include 'level' column here

-- Set competition_id as PRIMARY KEY
ALTER TABLE competitions
    ADD CONSTRAINT competitions_pkey PRIMARY KEY (competition_id);

-- Add foreign key constraint for category_id referencing categories
ALTER TABLE competitions
    ADD CONSTRAINT fk_category_id FOREIGN KEY (category_id)
    REFERENCES categories (category_id) ON DELETE SET NULL;

SELECT * FROM complexes
SELECT * FROM venues

--1.Modify complexes table
-- Change the data types and set constraints
ALTER TABLE complexes
    ALTER COLUMN complex_id SET DATA TYPE VARCHAR(50),
    ALTER COLUMN complex_name SET DATA TYPE VARCHAR(100);

-- Set primary key for complex_id
ALTER TABLE complexes
    ADD CONSTRAINT pk_complex_id PRIMARY KEY (complex_id);

-- 2. Modify the Venues Table
-- Change the data types and set constraints
ALTER TABLE venues
    ALTER COLUMN venue_id SET DATA TYPE VARCHAR(50),
    ALTER COLUMN venue_name SET DATA TYPE VARCHAR(100),
    ALTER COLUMN city_name SET DATA TYPE VARCHAR(100),
    ALTER COLUMN country_name SET DATA TYPE VARCHAR(100),
    ALTER COLUMN country_code SET DATA TYPE CHAR(3),
    ALTER COLUMN timezone SET DATA TYPE VARCHAR(100),
    ALTER COLUMN complex_id SET DATA TYPE VARCHAR(50);

-- Set primary key for venue_id
ALTER TABLE venues
    ADD CONSTRAINT pk_venue_id PRIMARY KEY (venue_id);

-- Set foreign key constraint to link venues with complexes
ALTER TABLE venues
    ADD CONSTRAINT fk_complex_id FOREIGN KEY (complex_id)
    REFERENCES complexes (complex_id)
    ON DELETE CASCADE;

SELECT * FROM competitors
SELECT * FROM competitor_rankings

-- Add rank_id column
ALTER TABLE competitor_rankings
    ADD COLUMN rank_id SERIAL PRIMARY KEY;

-- Alter Competitor_Rankings Table to Set Data Types and Constraints
ALTER TABLE competitor_rankings
    ALTER COLUMN rank SET DATA TYPE INT,
    ALTER COLUMN movement SET DATA TYPE INT,
    ALTER COLUMN points SET DATA TYPE INT,
    ALTER COLUMN competitions_played SET DATA TYPE INT,
    ALTER COLUMN competitor_id SET DATA TYPE VARCHAR(50);


--Adding primary key
ALTER TABLE competitors
    ADD PRIMARY KEY (competitor_id);

-- Add Foreign Key Constraint on competitor_id
ALTER TABLE competitor_rankings
    ADD CONSTRAINT fk_competitor_id FOREIGN KEY (competitor_id)
    REFERENCES competitors (competitor_id)
    ON DELETE CASCADE;  -- Ensure that if a competitor is deleted, their ranking data is also deleted