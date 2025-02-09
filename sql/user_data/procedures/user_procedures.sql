-- Drop existing procedures if they exist
DO $$ 
BEGIN
    DROP PROCEDURE IF EXISTS bot.upsert_user_profile;
    DROP PROCEDURE IF EXISTS bot.record_simulation;
    DROP FUNCTION IF EXISTS bot.get_user_profile;
    DROP FUNCTION IF EXISTS bot.get_user_simulations;
EXCEPTION
    WHEN OTHERS THEN NULL;
END $$;

-- Procedure to insert or update user profile
CREATE OR REPLACE PROCEDURE bot.upsert_user_profile(
    IN p_user_id BIGINT,
    IN p_username TEXT,
    IN p_first_name TEXT,
    IN p_last_name TEXT,
    IN p_current_city TEXT,
    IN p_current_country TEXT,
    IN p_current_occupation TEXT DEFAULT NULL,
    IN p_monthly_income DECIMAL DEFAULT NULL,
    IN p_currency TEXT DEFAULT 'USD'
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO bot.user_profiles (
        user_id, username, first_name, last_name,
        current_city, current_country, current_occupation,
        monthly_income, currency, updated_at
    )
    VALUES (
        p_user_id, p_username, p_first_name, p_last_name,
        p_current_city, p_current_country, p_current_occupation,
        p_monthly_income, p_currency, CURRENT_TIMESTAMP
    )
    ON CONFLICT (user_id) DO UPDATE SET
        username = EXCLUDED.username,
        first_name = EXCLUDED.first_name,
        last_name = EXCLUDED.last_name,
        current_city = EXCLUDED.current_city,
        current_country = EXCLUDED.current_country,
        current_occupation = EXCLUDED.current_occupation,
        monthly_income = EXCLUDED.monthly_income,
        currency = EXCLUDED.currency,
        updated_at = CURRENT_TIMESTAMP;
END;
$$;

-- Function to get user profile
CREATE OR REPLACE FUNCTION bot.get_user_profile(
    IN p_user_id BIGINT
)
RETURNS TABLE (
    user_id BIGINT,
    username TEXT,
    first_name TEXT,
    last_name TEXT,
    current_city TEXT,
    current_country TEXT,
    current_occupation TEXT,
    monthly_income DECIMAL,
    currency TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT *
    FROM bot.user_profiles
    WHERE user_profiles.user_id = p_user_id;
END;
$$;

-- Procedure to record simulation
CREATE OR REPLACE PROCEDURE bot.record_simulation(
    IN p_user_id BIGINT,
    IN p_simulation_type TEXT,
    IN p_source_city TEXT,
    IN p_target_city TEXT,
    IN p_source_occupation TEXT DEFAULT NULL,
    IN p_target_occupation TEXT DEFAULT NULL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO bot.simulations (
        user_id, simulation_type, source_city,
        target_city, source_occupation, target_occupation
    )
    VALUES (
        p_user_id, p_simulation_type, p_source_city,
        p_target_city, p_source_occupation, p_target_occupation
    );
END;
$$;

-- Function to get user's recent simulations
CREATE OR REPLACE FUNCTION bot.get_user_simulations(
    IN p_user_id BIGINT,
    IN p_limit INTEGER DEFAULT 5
)
RETURNS TABLE (
    id INTEGER,
    user_id BIGINT,
    simulation_type TEXT,
    source_city TEXT,
    target_city TEXT,
    source_occupation TEXT,
    target_occupation TEXT,
    simulated_at TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT s.*
    FROM bot.simulations s
    WHERE s.user_id = p_user_id
    ORDER BY s.simulated_at DESC
    LIMIT p_limit;
END;
$$;

-- Function to check if user exists
CREATE OR REPLACE FUNCTION bot.user_exists(
    IN p_user_id BIGINT
)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1
        FROM bot.user_profiles
        WHERE user_id = p_user_id
    );
END;
$$;
