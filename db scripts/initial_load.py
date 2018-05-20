import json as simplejson
from sodapy import Socrata
import MySQLdb

dbname = 'chuckauey'
dbuser = 'root'
dbpass = 'password'
dbhost = 'localhost'

try:
    client = Socrata("data.melbourne.vic.gov.au", None)
    parking_bay = client.get("vh2v-4nfs", limit=5000)
    print (len(parking_bay))
    #print (parking_bay)
    parking_data = []
    for item in parking_bay:
        bay_id=float(item['bay_id'])
        st_marker_id=str(item['st_marker_id'])
        status=str(item['status'])
        lon = float(item['lon'])
        lat= float(item['lat'])
        location = "("+ str(item['lat'])+","+str(item['lon'])+")"
        data_bind = (bay_id,st_marker_id,status,location,lat,lon)
        parking_data.append(data_bind)
    #print (parking_data)
    dbconn=MySQLdb.connect(
      db=dbname, user=dbuser, passwd=dbpass, host=dbhost)


    query = "INSERT INTO onstreet_parking_bay_sensors(Bay_id,St_marker_id,Status,Location,Lat,Lon) VALUES (%s,%s,%s,%s,%s,%s)"

    cur = dbconn.cursor()
    # Use all the SQL you like
    cur.executemany(query, parking_data)

    # print all the first cell of all the rows
    #for row in cur.fetchall():
    #    print (row)
    dbconn.commit()
    #dbconn.close()
except Exception as e:
    print (e)
finally:
    cur.close()
    dbconn.close()