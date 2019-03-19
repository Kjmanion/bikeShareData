import csv
import psycopg2

placeNums = {}

connection = psycopg2.connect("dbname=edinburgh user=postgres password=postgres host=localhost")    
cur = connection.cursor()


cur.execute("SELECT * FROM bikeroutes")
routes = cur.fetchall()
for route in routes:
    if route[4] != None:
        print (route[0], route[1], route[4])
        cur.execute("""UPDATE biketrips SET geom = %s WHERE startloc = %s AND endloc = %s
            """, (route[4], route[0], route[1]))

connection.commit()
cur.close()
connection.close