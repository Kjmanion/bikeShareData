import csv
import psycopg2

# In pgRouting, an ID is given to each street segment. This script will take the line closest to each stop and find the ID of that and populate the table with it.

connection = psycopg2.connect("dbname=edinburgh user=postgres password=postgres host=localhost")    
cur = connection.cursor()


# Selecting all the bikestop names and putting them into a python list
cur.execute("SELECT * FROM bikestops;")
list2 = cur.fetchall()
stopNames = []
for item in list2:
    stopNames.append(item[1])

# Prepping a dict for a key to the stop name and the value to be geometry of the closest point/street created when executing the sql query directly below
stopLocations = {}

for name in stopNames:
    cur.execute("""SELECT st_closestpoint(streets.geom, (SELECT bikeStops.geom
        FROM bikestops
        WHERE bikestops.stopname = %s)) as closes, source, target, ST_Distance(streets.geom, (
        SELECT bikeStops.geom
        FROM bikestops
        WHERE bikestops.stopname = %s))
        FROM streets
        ORDER BY ST_Distance 
        LIMIT 1;""", (name, name))
    answer = cur.fetchone()
    stopLocations[name] = answer
    print (answer)


# Selecting the node for each unique route to create a route using the pgRouting query below
cur.execute("SELECT startnodenum, endnodenum FROM bikeroutes")
answer =cur.fetchall()
for coors in answer:
    print (coors)
    cur.execute("""SELECT ST_Union(geom) FROM 
        (SELECT seq, id1 AS node, id2 AS edge, cost, geom, row_number() over() as qgis_id

        FROM pgr_dijkstra(

        'SELECT id, source, target, st_length(geom) as cost FROM public.streets', %s, %s, false, false

        ) AS di 

        JOIN public.streets pt

        ON di.id2 = pt.id) AS routes;
    """, (coors[0], coors[1],))
    geom = cur.fetchone()
    print (geom)
    cur.execute("""UPDATE bikeroutes SET geom = %s WHERE startnodenum = %s AND endnodenum = %s
    """, (geom, coors[0], coors[1]))




connection.commit()
cur.close()
connection.close