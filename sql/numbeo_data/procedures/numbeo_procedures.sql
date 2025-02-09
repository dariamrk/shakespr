DO $$ 
BEGIN
    DROP PROCEDURE IF EXISTS numbeo_col.insert_update_data;
    DROP PROCEDURE IF EXISTS numbeo_col.insert_restaurant_data;
    DROP PROCEDURE IF EXISTS numbeo_col.insert_market_data;
    DROP PROCEDURE IF EXISTS numbeo_col.insert_transportation_data;
    DROP PROCEDURE IF EXISTS numbeo_col.insert_utilities_data;
    DROP PROCEDURE IF EXISTS numbeo_col.insert_leisure_data;
    DROP PROCEDURE IF EXISTS numbeo_col.insert_clothing_data;
    DROP PROCEDURE IF EXISTS numbeo_col.insert_rent_data;
EXCEPTION
    WHEN OTHERS THEN NULL;
END $$;

-- Insert update record
CREATE OR REPLACE PROCEDURE numbeo_col.insert_update_data(
    IN p_city_id INTEGER,
    IN p_date TIMESTAMP
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO numbeo_col.updates (city_id, date)
    VALUES (p_city_id, p_date);
END;
$$;

-- Insert restaurant costs
CREATE OR REPLACE PROCEDURE numbeo_col.insert_restaurant_data(
    IN p_cheap_meal_for_one DECIMAL,
    IN p_meal_for_two DECIMAL,
    IN p_mcdonalds_meal DECIMAL,
    IN p_domestic_beer DECIMAL,
    IN p_imported_beer DECIMAL,
    IN p_cappuccino DECIMAL,
    IN p_coke_or_pepsi DECIMAL,
    IN p_water DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO numbeo_col.restaurant_cost_sets
    VALUES (
        (SELECT MAX(update_id) FROM numbeo_col.updates),
        p_cheap_meal_for_one,
        p_meal_for_two,
        p_mcdonalds_meal,
        p_domestic_beer,
        p_imported_beer,
        p_cappuccino,
        p_coke_or_pepsi,
        p_water
    );
END;
$$;

-- Insert market costs
CREATE OR REPLACE PROCEDURE numbeo_col.insert_market_data(
    IN p_milk_one_liter DECIMAL,
    IN p_bread_loaf DECIMAL,
    IN p_white_rice_one_kg DECIMAL,
    IN p_dozen_eggs DECIMAL,
    IN p_cheese_one_kg DECIMAL,
    IN p_chicken_breast_one_kg DECIMAL,
    IN p_beef_round_one_kg DECIMAL,
    IN p_apples_one_kg DECIMAL,
    IN p_bananas_one_kg DECIMAL,
    IN p_oranges_one_kg DECIMAL,
    IN p_tomatoes_one_kg DECIMAL,
    IN p_potatoes_one_kg DECIMAL,
    IN p_onions_one_kg DECIMAL,
    IN p_lettuce_head DECIMAL,
    IN p_water_one_and_half_liter DECIMAL,
    IN p_wine_mid_range DECIMAL,
    IN p_domestic_beer_half_liter DECIMAL,
    IN p_imported_beer_third_liter DECIMAL,
    IN p_cigarettes_pack DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO numbeo_col.market_cost_sets
    VALUES (
        (SELECT MAX(update_id) FROM numbeo_col.updates),
        p_milk_one_liter,
        p_bread_loaf,
        p_white_rice_one_kg,
        p_dozen_eggs,
        p_cheese_one_kg,
        p_chicken_breast_one_kg,
        p_beef_round_one_kg,
        p_apples_one_kg,
        p_bananas_one_kg,
        p_oranges_one_kg,
        p_tomatoes_one_kg,
        p_potatoes_one_kg,
        p_onions_one_kg,
        p_lettuce_head,
        p_water_one_and_half_liter,
        p_wine_mid_range,
        p_domestic_beer_half_liter,
        p_imported_beer_third_liter,
        p_cigarettes_pack
    );
END;
$$;

-- Insert transportation costs
CREATE OR REPLACE PROCEDURE numbeo_col.insert_transportation_data(
    IN p_local_transit_one_way DECIMAL,
    IN p_monthly_transit_pass DECIMAL,
    IN p_taxi_base_fare DECIMAL,
    IN p_taxi_one_km DECIMAL,
    IN p_taxi_one_hr DECIMAL,
    IN p_gasoline_one_liter DECIMAL,
    IN p_volkswagen_golf DECIMAL,
    IN p_toyota_corolla DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO numbeo_col.transportation_cost_sets
    VALUES (
        (SELECT MAX(update_id) FROM numbeo_col.updates),
        p_local_transit_one_way,
        p_monthly_transit_pass,
        p_taxi_base_fare,
        p_taxi_one_km,
        p_taxi_one_hr,
        p_gasoline_one_liter,
        p_volkswagen_golf,
        p_toyota_corolla
    );
END;
$$;

-- Insert utilities costs
CREATE OR REPLACE PROCEDURE numbeo_col.insert_utilities_data(
    IN p_all_basic DECIMAL,
    IN p_prepaid_mobile_one_min DECIMAL,
    IN p_internet_sixty_mbps DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO numbeo_col.utilities_cost_sets
    VALUES (
        (SELECT MAX(update_id) FROM numbeo_col.updates),
        p_all_basic,
        p_prepaid_mobile_one_min,
        p_internet_sixty_mbps
    );
END;
$$;

-- Insert leisure costs
CREATE OR REPLACE PROCEDURE numbeo_col.insert_leisure_data(
    IN p_fit_club_one_month DECIMAL,
    IN p_tennis_court_one_hr DECIMAL,
    IN p_cinema_ticket_one_seat DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO numbeo_col.leisure_cost_sets
    VALUES (
        (SELECT MAX(update_id) FROM numbeo_col.updates),
        p_fit_club_one_month,
        p_tennis_court_one_hr,
        p_cinema_ticket_one_seat
    );
END;
$$;

-- Insert clothing costs
CREATE OR REPLACE PROCEDURE numbeo_col.insert_clothing_data(
    IN p_pair_of_jeans DECIMAL,
    IN p_summer_dress DECIMAL,
    IN p_nike_running_shoes DECIMAL,
    IN p_leather_business_shoes DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO numbeo_col.clothing_cost_sets
    VALUES (
        (SELECT MAX(update_id) FROM numbeo_col.updates),
        p_pair_of_jeans,
        p_summer_dress,
        p_nike_running_shoes,
        p_leather_business_shoes
    );
END;
$$;

-- Insert rent costs
CREATE OR REPLACE PROCEDURE numbeo_col.insert_rent_data(
    IN p_apt_one_bdrm_ctr DECIMAL,
    IN p_apt_one_bdrm_out DECIMAL,
    IN p_apt_three_bdrm_ctr DECIMAL,
    IN p_apt_three_bdrm_out DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO numbeo_col.rent_cost_sets
    VALUES (
        (SELECT MAX(update_id) FROM numbeo_col.updates),
        p_apt_one_bdrm_ctr,
        p_apt_one_bdrm_out,
        p_apt_three_bdrm_ctr,
        p_apt_three_bdrm_out
    );
END;
$$;
