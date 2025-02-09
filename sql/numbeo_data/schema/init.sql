-- Create schema
CREATE SCHEMA IF NOT EXISTS numbeo_col;

-- Set timezone
SET timezone = 'UTC';

-- Create cities table with unique constraint
CREATE TABLE IF NOT EXISTS numbeo_col.cities (
    city_id SMALLSERIAL PRIMARY KEY,
    city_name VARCHAR(45) NOT NULL,
    country VARCHAR(45) NOT NULL,
    region VARCHAR(45) NOT NULL,
    UNIQUE(city_name, country)  -- Add unique constraint
);

-- Create updates table
CREATE TABLE IF NOT EXISTS numbeo_col.updates (
    update_id SERIAL PRIMARY KEY,
    city_id SMALLINT NOT NULL,
    date TIMESTAMP NOT NULL,
    CONSTRAINT fk_updates_cities 
        FOREIGN KEY (city_id) 
        REFERENCES numbeo_col.cities(city_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create clothing_cost_sets table
CREATE TABLE IF NOT EXISTS numbeo_col.clothing_cost_sets (
    update_id INTEGER PRIMARY KEY,
    pair_of_jeans DECIMAL(5,2),
    summer_dress DECIMAL(5,2),
    nike_running_shoes DECIMAL(5,2),
    leather_business_shoes DECIMAL(5,2),
    CONSTRAINT fk_clothing_cost_sets_updates
        FOREIGN KEY (update_id)
        REFERENCES numbeo_col.updates(update_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create rent_cost_sets table
CREATE TABLE IF NOT EXISTS numbeo_col.rent_cost_sets (
    update_id INTEGER PRIMARY KEY,
    apt_one_bdrm_ctr DECIMAL(7,2),
    apt_one_bdrm_out DECIMAL(7,2),
    apt_three_bdrm_ctr DECIMAL(7,2),
    apt_three_bdrm_out DECIMAL(7,2),
    CONSTRAINT fk_rent_cost_sets_updates
        FOREIGN KEY (update_id)
        REFERENCES numbeo_col.updates(update_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create utilities_cost_sets table
CREATE TABLE IF NOT EXISTS numbeo_col.utilities_cost_sets (
    update_id INTEGER PRIMARY KEY,
    all_basic DECIMAL(6,2),
    prepaid_mobile_one_min DECIMAL(4,2),
    internet_sixty_mbps DECIMAL(5,2),
    CONSTRAINT fk_utilities_cost_sets_updates
        FOREIGN KEY (update_id)
        REFERENCES numbeo_col.updates(update_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create leisure_cost_sets table
CREATE TABLE IF NOT EXISTS numbeo_col.leisure_cost_sets (
    update_id INTEGER PRIMARY KEY,
    fit_club_one_month DECIMAL(5,2),
    tennis_court_one_hr DECIMAL(5,2),
    cinema_ticket_one_seat DECIMAL(4,2),
    CONSTRAINT fk_leisure_cost_sets_updates
        FOREIGN KEY (update_id)
        REFERENCES numbeo_col.updates(update_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create restaurant_cost_sets table
CREATE TABLE IF NOT EXISTS numbeo_col.restaurant_cost_sets (
    update_id INTEGER PRIMARY KEY,
    cheap_meal_for_one DECIMAL(5,2),
    meal_for_two DECIMAL(5,2),
    mcdonalds_meal DECIMAL(4,2),
    domestic_beer DECIMAL(4,2),
    imported_beer DECIMAL(4,2),
    cappuccino DECIMAL(4,2),
    coke_or_pepsi DECIMAL(4,2),
    water DECIMAL(4,2),
    CONSTRAINT fk_restaurant_cost_sets_updates
        FOREIGN KEY (update_id)
        REFERENCES numbeo_col.updates(update_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create market_cost_sets table
CREATE TABLE IF NOT EXISTS numbeo_col.market_cost_sets (
    update_id INTEGER PRIMARY KEY,
    milk_one_liter DECIMAL(4,2),
    bread_loaf DECIMAL(4,2),
    white_rice_one_kg DECIMAL(4,2),
    dozen_eggs DECIMAL(4,2),
    cheese_one_kg DECIMAL(5,2),
    chicken_breast_one_kg DECIMAL(4,2),
    beef_round_one_kg DECIMAL(4,2),
    apples_one_kg DECIMAL(4,2),
    bananas_one_kg DECIMAL(4,2),
    oranges_one_kg DECIMAL(4,2),
    tomatoes_one_kg DECIMAL(4,2),
    potatoes_one_kg DECIMAL(4,2),
    onions_one_kg DECIMAL(4,2),
    lettuce_head DECIMAL(4,2),
    water_one_and_half_liter DECIMAL(4,2),
    wine_mid_range DECIMAL(5,2),
    domestic_beer_half_liter DECIMAL(4,2),
    imported_beer_third_liter DECIMAL(4,2),
    cigarettes_pack DECIMAL(4,2),
    CONSTRAINT fk_market_cost_sets_updates
        FOREIGN KEY (update_id)
        REFERENCES numbeo_col.updates(update_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- Create transportation_cost_sets table
CREATE TABLE IF NOT EXISTS numbeo_col.transportation_cost_sets (
    update_id INTEGER PRIMARY KEY,
    local_transit_one_way DECIMAL(4,2),
    monthly_transit_pass DECIMAL(5,2),
    taxi_base_fare DECIMAL(4,2),
    taxi_one_km DECIMAL(4,2),
    taxi_one_hr DECIMAL(5,2),
    gasoline_one_liter DECIMAL(4,2),
    volkswagen_golf DECIMAL(8,2),
    toyota_corolla DECIMAL(8,2),
    CONSTRAINT fk_transportation_cost_sets_updates
        FOREIGN KEY (update_id)
        REFERENCES numbeo_col.updates(update_id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
