import psycopg2
import httplib2
import json
from ast import literal_eval

with open('sql/region/insert_region.sql', 'r') as region_insert_file:
    region_insert_query = region_insert_file.read()
conn_string = "host='localhost' dbname='arbitrage' user='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
print("Connected to postgres!")
h = httplib2.Http(".cache")
regions_response, content = h.request("https://esi.tech.ccp.is/latest/universe/regions/?datasource=tranquility", "GET")
regions = literal_eval(content.decode('utf-8'))
print("Queried Regions list from CCP!")
for region in regions:
    region_response, region_content = h.request("https://esi.tech.ccp.is/latest/universe/regions/"+ str(region)+"/?datasource=tranquility&language=en-us","GET")
    region_pretty = literal_eval(region_content.decode('utf-8'))
    region_pretty.setdefault('description', "none")
    cursor.execute(region_insert_query,(region_pretty['region_id'],region_pretty['description'],region_pretty['name']))
    conn.commit()
