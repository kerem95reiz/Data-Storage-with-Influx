from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from db import create_db, get_dbs, delete_db, write_data, read_data, get_measurements, read_latest_entries, read_criteria, query, read_last_entries
from traceback import print_exc

app = Flask(__name__)
api = Api(app)


class NewDb(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        super(NewDb, self).__init__()
    
    def post(self):
        args = self.reqparser.parse_args()
        # Error checking: Whether a name is entered
        if args['db_name'] is None:
            return {'Error': 'Please enter a db_name'}

        db_name = args['db_name']
        result = create_db(db_name)
        return result

class GetDBs(Resource):

    def __init__(self):
        super(GetDBs, self).__init__()

    def get(self):
        dbs = get_dbs()
        return {"Existing Databases": dbs}

class DeleteDB(Resource):

    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        super(DeleteDB, self).__init__()

    def post(self):
        args = self.reqparser.parse_args()

        if args['db_name'] is None:
            return {'Error': 'Please enter a db_name'}

        db_name = args['db_name']   
        result = delete_db(db_name)

        return str(result)

class GetMeasurements(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        super(GetMeasurements, self).__init__()


    def get(self):
        
        args = self.reqparser.parse_args()
        # print(args)

        if args['db_name'] is None:
            return {'Error': 'Please enter a db_name'}

        db_name = args['db_name']
        result = get_measurements(db_name)

        return result

class WriteReadData(Resource):

    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.reqparser.add_argument('measurement', type=str, help='Name of the measurement')
        self.reqparser.add_argument('data', type=str, location='json')
        super(WriteReadData, self).__init__()

    def post(self):
        args = self.reqparser.parse_args()
        db_name = args['db_name']
        json_data = request.get_json()
        result = False
        # print("By write request the db name is:", db_name )
        try:
            result = write_data(json_data, db_name)
        except:
            print_exc()

        if result is not True:
            return str(result)

        return True

    def get(self):
        args = self.reqparser.parse_args()
        db_name = args['db_name']
        measurement = args['measurement']

        try:
            result = read_data(db_name, measurement)
        except Exception:
            print_exc()
            raise Exception

        return str(result)

class ReadLatestEntries(Resource):
        def __init__(self):
            self.reqparser = reqparse.RequestParser()
            self.reqparser.add_argument('db_name', type=str, help='Name of the database')
            self.reqparser.add_argument('measurement', type=str, help='Name of the measurement')
            self.reqparser.add_argument('period', type=str, help='Frequency for reading')
            self.reqparser.add_argument('current_time', type=str, help='Current time')
            super(ReadLatestEntries, self).__init__()

        def get(self):
            args = self.reqparser.parse_args()
            db_name = args['db_name']
            measurement = args['measurement']
            period = 1000000000 * int(args['period'])
            current_time = int(args['current_time'])
            try:
                latest_entries = read_latest_entries(db_name, measurement, period, current_time)
            except Exception:
                print_exc()
                raise Exception
            return jsonify(latest_entries)

class ReadLastEntries(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.reqparser.add_argument('measurement', type=str, help='Name of the measurement')
        super(ReadLastEntries, self).__init__()

    def get(self):
        args = self.reqparser.parse_args()
        db_name = args['db_name']
        measurement = args['measurement']

        try:
            last_entries = read_last_entries(db_name, measurement)
        except:
            print_exc()
            raise Exception
        return jsonify(last_entries)

class Criteria(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.reqparser.add_argument('measurement', type=str, help='Name of the measurement')
        super(Criteria, self).__init__()

    def get(self):
        args = self.reqparser.parse_args()
        db_name = args['db_name']
        measurement = args['measurement']
        try:
            criteria = read_criteria(db_name, measurement)
        except Exception:
            print_exc()
            raise Exception
        return criteria
    
class Query(Resource):
    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.reqparser.add_argument('measurement', type=str, help='Name of the measurement')
        self.reqparser.add_argument('query', type=str)
        super(Query, self).__init__()

    def get(self):
        args = self.reqparser.parse_args()
        db_name = args['db_name']
        measurement = args['measurement']
        query_str = args['query']

        try:
            r = query(db_name, measurement, query_str)
        except Exception:
            print_exc()
            raise Exception
        return r


api.add_resource(NewDb, '/newdb')
api.add_resource(GetDBs, '/getdbs')
api.add_resource(DeleteDB, '/deletedb')
api.add_resource(WriteReadData, '/writereaddata')
api.add_resource(GetMeasurements, '/getmeasurements')
api.add_resource(ReadLatestEntries, '/readlatestentries')
api.add_resource(ReadLastEntries, '/readlastentries')
api.add_resource(Criteria, '/criteria')
api.add_resource(Query, '/query')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4545)