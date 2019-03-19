

import csv
import psycopg2


connection = psycopg2.connect("dbname=edinburgh user=postgres password=postgres host=localhost")    
cur = connection.cursor()

places = {}
with open(r'D:\GIS Data\Edinburgh\January.csv', newline='') as csvfile:
    readFile = csv.reader(csvfile, delimiter=',')
    next(readFile)
    for row in readFile:
        # Getting all the unique bikestops to be put into it's own table, bikestops, with the name, description, and coordinates of the stop
        if row[4] not in places:
            places[row[4]] = [row[5], row[6], row[7]]
        # Putting all the trips into a postgres table
        cur.execute("""INSERT INTO biketrips (starttime, endtime, startloc, endloc) 
                    VALUES (%s, %s, %s, %s)
                    """, (row[0], row[1], row[4], row[9]))



# Entering bikestops data into bikestops table

connection = psycopg2.connect("dbname=edinburgh user=postgres password=postgres host=localhost")    
cur = connection.cursor()
for place in places:
    if 'start' in places[place][1]:
        print ('wrong')
    else: 
      
        cur.execute("""INSERT INTO bikestops (stopname, stopdesc, geom) 
                    VALUES (%s, %s, ST_GeomFromText('POINT(%s %s)', 4326))
                    """, (place, places[place][0], float(places[place][2]), float(places[place][1])))
print (sql)
connection.commit()
cur.close()
connection.close



