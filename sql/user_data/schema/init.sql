-- Drop existing objects if they exist
DO $$ 
BEGIN
    -- Drop trigger if exists
    IF EXISTS (
        SELECT 1 FROM pg_trigger 
        WHERE tgname = 'update_user_profiles_updated_at'
    ) THEN
        DROP TRIGGER IF EXISTS update_user_profiles_updated_at ON bot.user_profiles;
    END IF;

    -- Drop function if exists
    DROP FUNCTION IF EXISTS bot.update_updated_at_column() CASCADE;
    
    -- Drop tables if they exist
    DROP TABLE IF EXISTS bot.simulations CASCADE;
    DROP TABLE IF EXISTS bot.user_profiles CASCADE;
    
    -- Drop schema if exists
    DROP SCHEMA IF EXISTS bot CASCADE;
EXCEPTION
    WHEN OTHERS THEN NULL;
END $$;

-- Create schema
CREATE SCHEMA IF NOT EXISTS bot;

-- User profiles table
CREATE TABLE IF NOT EXISTS bot.user_profiles (
    user_id BIGINT PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    current_city TEXT NOT NULL,
    current_country TEXT NOT NULL,
    current_occupation TEXT,
    monthly_income DECIMAL(10,2),
    currency TEXT DEFAULT 'USD',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Simulation history table
CREATE TABLE IF NOT EXISTS bot.simulations (
    id SERIAL PRIMARY KEY,
    user_id BIGINT REFERENCES bot.user_profiles(user_id),
    simulation_type TEXT NOT NULL, -- 'relocation' or 'career'
    source_city TEXT NOT NULL,
    target_city TEXT NOT NULL,
    source_occupation TEXT,
    target_occupation TEXT,
    simulated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create update timestamp function
CREATE OR REPLACE FUNCTION bot.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for updating timestamp
CREATE TRIGGER update_user_profiles_updated_at
    BEFORE UPDATE ON bot.user_profiles
    FOR EACH ROW
    EXECUTE FUNCTION bot.update_updated_at_column();
