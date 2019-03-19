import csv
import psycopg2

placeNums = {}

connection = psycopg2.connect("dbname=edinburgh user=postgres password=postgres host=localhost")    
cur = connection.cursor()
cur.execute("SELECT * FROM bikestops;")
bikestopsAll = cur.fetchall()
stopNames = []
for item in bikestopsAll:
    stopNames.append(item[1])


def getAllRoutes(bikeStops):
    # Takes an input of bikeStops, which is a list of all the bikestops in the city to create all possible routes from one bikestop to another. Then adds
    # them to a new list
    routes = []
    for item in bikeStops:
        print (item)
        for j in bikeStops:
            newRoute = frozenset((item, j))
            routes.append(newRoute)
    
    return routes

routes = getAllRoutes(stopNames)
print (len(routes))
for route in routes:
    x = route
    startPt, *_ = x 
    *_, endPt = x
    print (startPt, endPt)
    cur.execute("""INSERT INTO bikeroutes (startpt, endpt) 
                    VALUES (%s, %s)
                    """, (startPt, endPt))






connection.commit()
cur.close()
connection.close
    