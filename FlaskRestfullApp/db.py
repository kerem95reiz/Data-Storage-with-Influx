from influxdb import InfluxDBClient

client = InfluxDBClient('db', 8086, 'root', 'root', 'example')


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
        print("Something went wrong during deletion of database!")
        return "Something went wrong during deletion of database!"
    
    return "Database deleted successfully"

def write_data(data_points, db_name):

    data = data_points['data']

    try:
        result = client.write_points(data, batch_size=10000, protocol=u'json', database=db_name)
    except:
        result = "Something went wrong during the write process!"
        print(result)

    return result

def read_data(db_name, measurement):

    query_all_table = 'SELECT * FROM ' + measurement

    if db_name not in get_dbs():
        return "Such a database does not exist!"

    try:
        data = client.query(query_all_table, database=db_name)
    except:
        data = "Something went wrong during read process"
        print(data)

    return data