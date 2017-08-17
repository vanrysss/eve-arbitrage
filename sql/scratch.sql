SELECT r.name, c.name, sys.name, stat.name FROM station stat
    JOIN star_system sys ON stat.eve_system_id = sys.eve_system_id
    JOIN constellation c ON sys.eve_constellation_id = c.eve_constellation_id
    JOIN region r ON c.eve_region_id = r.eve_region_id
    WHERE stat.eve_station_id=61000710;

SELECT m.price,m.volume_remain, s.name FROM market_order m 
    JOIN station s ON s.eve_station_id = m.location_id
    JOIN star_system sys ON s.eve_system_id = sys.eve_system_id
    WHERE m.is_buy_order = FALSE 
    AND sys.security_status > 0.5
ORDER BY m.price ASC LIMIT 10;

SELECT m.price,m.volume_remain, s.name FROM market_order m 
    JOIN station s ON s.eve_station_id = m.location_id
    JOIN star_system sys ON s.eve_system_id = sys.eve_system_id
    WHERE m.is_buy_order = TRUE 
    AND sys.security_status > 0.5
ORDER BY m.price DESC LIMIT 5;

SELECT * FROM market_order WHERE is_buy_order = FALSE ORDER BY price ASC LIMIT 1;
