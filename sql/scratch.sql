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

SELECT sys.name FROM star_system sys
    JOIN constellation c ON sys.eve_constellation_id = c.eve_constellation_id
    JOIN (SELECT * FROM region WHERE name ='Curse') AS r
    ON c.eve_region_id = r.eve_region_id
    WHERE sys.security_status > -0.1;

SELECT r.name,stat.name FROM station stat    
    JOIN star_system s ON stat.eve_system_id = s.eve_system_id
    JOIN constellation c ON s.eve_constellation_id = c.eve_constellation_id
    JOIN region r ON c.eve_region_id = r.eve_region_id
    WHERE stat.eve_station_id = 60014945;

#filter out non sec-space stations
SELECT count(1), r.name FROM star_system sys
    JOIN constellation c ON sys.eve_constellation_id = c.eve_constellation_id
    JOIN region r ON c.eve_region_id = r.eve_region_id
    WHERE sys.security_status > 0.0
    GROUP BY r.name;    

#core functionality query
SELECT i.name, 
        sale.volume_remain, 
        buy.volume_remain, 
        sale.price AS sale_price, 
        buy.price AS buy_price, 
        sale_stat.name AS sale_station, 
        buy_stat.name AS buy_station, 
        buy.eve_order_id, 
        sale.eve_order_id,
        (SELECT LEAST(buy.volume_remain, sale.volume_remain) * (buy.price - sale.price)) AS profit
    FROM market_order sale
    JOIN item i ON sale.item_type_id = i.type_id
    JOIN market_order buy ON sale.item_type_id = buy.item_type_id
    JOIN station buy_stat ON buy.location_id = buy_stat.eve_station_id
    JOIN station sale_stat ON sale.location_id = sale_stat.eve_station_id
    WHERE sale.is_buy_order = FALSE
    AND buy.is_buy_order = TRUE
    AND buy.price > sale.price
    ORDER BY profit DESC;