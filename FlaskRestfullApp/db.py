from influxdb import InfluxDBClient

client = InfluxDBClient('db', 8086, 'root', 'root', 'example')


def db_ops():

    json_body = [
        {
            "measurement": "computer",
            "fields": {
                "value": "macbook"
            }
        }
    ]

    # client = InfluxDBClient('172.18.0.3', 8086, 'root', 'root', 'example')
    client = InfluxDBClient('db', 8086, 'root', 'root', 'example')

    client.create_database('example')

    client.write_points(json_body)

    result = client.query('SELECT value FROM computer')

    print("Results are ", result)
    return str(result)

    # Check whether the db already exists

def create_db(db_name):

    # Just to get the name of the databases, insead of a another data structure
    dbs = get_dbs()
    if db_name in dbs:
        return "Already exists"

    try:
        client.create_database(db_name)
    except:
        return "Something went wrong during creating a new database"


    return "A new db with the name " + db_name + " created"

def get_dbs():

    try:
        databases = client.get_list_database()
    except:
        return "Something went wrong during reading list of databases"


    dbs = [key['name'] for key in databases] 
    return dbs

def delete_db(db_name):
    
    # check whether the db already exits
    dbs = get_dbs()
    if db_name not in dbs:
        return "DB does not exist!"
    
    try:
        client.drop_database(db_name)
    except:
        print("Something went wrong")
        return "Something went wrong during deletion of database!"
    
    return "Database deleted successfully"


    #If yes, then delete the db

def write_data(data_points, db_name):

    return True

# Sample Data Format
# {
# 		"thread": 1,
# 		"priority": 80,
# 		"I": 200,
# 		"C": 500,
# 		"max_latency": 10,
# 		"min_latency": 10,
# 		"avg_latency": 10,
# 		"act_latency": 10
# 	}