import psycopg2
import requests
import json
from ast import literal_eval


with open('sql/order/insert_order.sql', 'r') as order_insert_file:
    order_insert_query = order_insert_file.read()

with open('sql/region/all_region_id_query.sql', 'r') as query_all_regions_file:
    all_regions_query = query_all_regions_file.read()
with open('sql/item/select_by_id.sql', 'r') as query_item_file:
    select_item_by_id = query_item_file.read()

conn_string = "host='localhost' dbname='arbitrage' user='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
print("Connected to postgres!")

cursor.execute(all_regions_query)
regions = cursor.fetchall()
for region in regions:
    item_id = 44992
    cursor.execute(select_item_by_id,([item_id]))
    item_type_id = cursor.fetchone()
    r = requests.get("https://esi.tech.ccp.is/dev/markets/" + str(region[0]) +"/orders/?datasource=tranquility&order_type=all&page=1&type_id=34828")
    if r.status_code == 200:
        for item in r.json():
            if item['location_id'] < 61001146:
                cursor.execute(order_insert_query,(item['duration'], item['is_buy_order'], item['issued'], item['location_id'], item['min_volume'], item['order_id'], item['price'],item['range'], item['type_id'],item['volume_remain'],item['volume_total']))
                conn.commit()
    else:
        print(r.status_code)