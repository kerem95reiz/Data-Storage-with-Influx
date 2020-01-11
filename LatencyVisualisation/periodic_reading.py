import time
import requests as req
import threading



def read_from_db(db_name, measurement, period, current_time):

    # fetch latest entries from the db
    # send the data to the visualisation container

    payload={'db_name': db_name, 'measurement': measurement, 'period': period, 'current_time': current_time}
    try:
        latest_entries = req.get('http://rest_api:4545/readlatestentries', params=payload)
    except:
        print("Error while sending data from rest api to visualisation service!")
        
    print("Latest Entries in Lat Vis: ", latest_entries.json())

    # TODO:...
    # Create a queue object in another file
    # Gain access to that object from here and save the requested data there
    # Then read the newly added data from the dash (app.py)


def periodic_reading(db_name, measurement, period):
    # InfluxDB works in nanoseconds, so time needs to be sent to db as nanoseconds as well
    current_time = time.time_ns()
    while True:
        payload={'db_name': db_name, 'measurement': measurement, 'period': period, 'current_time': current_time}
        try:
            latest_entries = req.get('http://rest_api:4545/readlatestentries', params=payload)
        except:
            print("Error while sending data from rest api to visualisation service!")
        
        print("Latest Entries in Lat Vis: ", latest_entries.json())

        time.sleep(period)
        current_time += period*1000000000


def start_reading(db_name, measurement, period):
    t = threading.Thread(target=periodic_reading, args=(db_name, measurement, period,))
    t.daemon = True
    t.start()