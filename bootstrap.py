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
with open('sql/station/insert_station.sql', 'r') as station_insert_file:
    station_insert_query = station_insert_file.read()
with open('sql/station/query_stations_by_system.sql', 'r') as station_query_file:
    station_query = station_query_file.read()


conn_string = "host='localhost' dbname='arbitrage' user='postgres'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
print("Connected to postgres!")
h = httplib2.Http(".cache")
'''
persist regional data
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
'''
'''
#persist constellation data
consellations_response, content = h.request("https://esi.tech.ccp.is/latest/universe/constellations/?datasource=tranquility", "GET")
constellations = literal_eval(content.decode('utf-8'))
print("Queried Constellations list from CCP!")
for constellation in constellations:
    constellation_response, constellation_content = h.request("https://esi.tech.ccp.is/dev/universe/constellations/"+ str(constellation) + "/?datasource=tranquility&language=en-us","GET")
    constellation_pretty = literal_eval(constellation_content.decode('utf-8'))
    print(constellation_pretty) 
    cursor.execute(constellation_insert_query,(constellation_pretty['constellation_id'], constellation_pretty['region_id'], constellation_pretty['name']))
    conn.commit()
    print("Constellation:" + constellation_pretty['name'])
'''
#persist system data
systems_response, systems_content = h.request("https://esi.tech.ccp.is/latest/universe/systems/?datasource=tranquility", "GET")
systems = literal_eval(systems_content.decode('utf-8'))
print("Queried Systems list from CCP!")
for system in systems:
    system_response, system_content = h.request("https://esi.tech.ccp.is/dev/universe/systems/"+ str(system) +"/?datasource=tranquility&language=en-us", "GET")
    s_pretty = literal_eval(system_content.decode('utf-8'))
    cursor.execute(system_insert_query,(s_pretty['system_id'],s_pretty['constellation_id'], s_pretty['name'], s_pretty['security_status']))
    conn.commit()
    print("System:" + s_pretty['name'])
    #persist station data
    if 'stations' in s_pretty:
        cursor.execute(station_query,([s_pretty['system_id']]))
        if cursor.fetchone() is None:
            stations_in_system = s_pretty['stations']
            for station in stations_in_system:
                station_reponse, station_content = h.request("https://esi.tech.ccp.is/dev/universe/stations/"+ str(station) + "/?datasource=tranquility","GET")
                station_pretty = literal_eval(station_content.decode('utf-8'))
                if 'name' in station_pretty:
                    cursor.execute(station_insert_query,(station_pretty['name'], station_pretty['station_id'],station_pretty['system_id']))
                    conn.commit()
                    print("Station:" + station_pretty['name'])

#persist market group data


#persist item data

