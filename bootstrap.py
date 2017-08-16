import psycopg2
import httplib2
import json
from ast import literal_eval

#imports all of the needed static data to postgres

with open('sql/region/insert_region.sql', 'r') as region_insert_file:
    region_insert_query = region_insert_file.read()
with open('sql/constellation/insert_constellation.sql', 'r') as constellation_insert_file:
    constellation_insert_query = constellation_insert_file.read()
with open('sql/system/insert_system.sql', 'r') as system_insert_file:
    system_insert_query = system_insert_file.read()

conn_string = "host='localhost' dbname='arbitrage' user='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
print("Connected to postgres!")
h = httplib2.Http(".cache")

#persist regional data
regions_response, content = h.request("https://esi.tech.ccp.is/latest/universe/regions/?datasource=tranquility", "GET")
regions = literal_eval(content.decode('utf-8'))
print("Queried Regions list from CCP!")
for region in regions:
    region_response, region_content = h.request("https://esi.tech.ccp.is/latest/universe/regions/"+ str(region) +"/?datasource=tranquility&language=en-us","GET")
    region_pretty = literal_eval(region_content.decode('utf-8'))
    region_pretty.setdefault('description', "none")
    cursor.execute(region_insert_query,(region_pretty['region_id'],region_pretty['description'],region_pretty['name']))
    conn.commit()
    print("Region:" + region_pretty['name'])

#persist constellation data
consellations_response, content = h.request("https://esi.tech.ccp.is/latest/universe/constellations/?datasource=tranquility", "GET")
constellations = literal_eval(content.decode('utf-8'))
print("Queried Constellations list from CCP!")
for constellation in constellations:
    constellation_response, constellation_content = h.request("https://esi.tech.ccp.is/latest/universe/constellations/"+ str(constellation) + "/?datasource=tranquility&language=en-us","GET")
    constellation_pretty = literal_eval(region_content.decode('utf-8'))
    cursor.execute(constellation_insert_query,(constellation_pretty['constellation_id'], constellation_pretty['region_id'], constellation_pretty['name'])
    conn.commit()
    print("Constellation:" + constellation_pretty['name'])

#persist system data
systems_response, system_content = h.request("https://esi.tech.ccp.is/latest/universe/systems/?datasource=tranquility", "GET")
systems = literal_eval(content.decode('utf-8'))
print("Queried Systems list from CCP!")
for system in systems:
    system_response, system_content = h.request("https://esi.tech.ccp.is/latest/universe/systems/"+ str(system) +"/?datasource=tranquility&language=en-us", "GET")
    s_pretty = literal_eval(system_content.decode('utf-8'))
    cursor.execute(system_insert_query,s_pretty['system_id'],s_pretty['constellation_id'], s_pretty['name'], s_pretty['security_class'], s_pretty['security_status'])
    conn.commit()
    print("System:" + s_pretty['name'])

#persist station data

#persist market group data

#persist item data

