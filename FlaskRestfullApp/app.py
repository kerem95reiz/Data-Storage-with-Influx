from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from db import create_db, get_dbs, delete_db, write_data, read_data

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

        try:
            result = write_data(json_data, db_name)
        except:
            print("Something went wrong during write process, in app.py")

        if result is not True:
            return str(result)

        return True

    def get(self):
        args = self.reqparser.parse_args()
        db_name = args['db_name']
        measurement = args['measurement']

        try:
            result = read_data(db_name, measurement)
        except:
            result = 'Something went wrong during read process!'
            print(result)

        return str(result)


api.add_resource(NewDb, '/newdb')
api.add_resource(GetDBs, '/getdbs')
api.add_resource(DeleteDB, '/deletedb')
api.add_resource(WriteReadData, '/writereaddata')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4545)