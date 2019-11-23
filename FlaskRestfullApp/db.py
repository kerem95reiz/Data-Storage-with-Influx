from influxdb import InfluxDBClient

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