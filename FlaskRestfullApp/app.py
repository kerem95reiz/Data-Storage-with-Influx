from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from db import db_ops, create_db, get_dbs, delete_db, write_data

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
# parser.add_argument('user', type=str, help='Username of the newly to be created user')
# parser.add_argument('password', type=str, help='Password')
parser.add_argument('db_name', type=str, help='Name of the new database')
# parser.add_argument('data_to_be_written', location='form', help='The data that wants to be written to a database')

class NewDb(Resource):
    
    def post(self):
        args = parser.parse_args()
        # Error checking
        if args['db_name'] is None:
            return {'Error': 'Please enter a db_name'}

        db_name = args['db_name']
        result = create_db(db_name)
        return result

class GetDBs(Resource):
    def get(self):
        dbs = get_dbs()
        return {"Existing Databases": dbs}

class DeleteDB(Resource):
    def post(self):
        args = parser.parse_args()

        if args['db_name'] is None:
            return {'Error': 'Please enter a db_name'}
        db_name = args['db_name']   
        result = delete_db(db_name)
        return "Massega is received"


class WriteData(Resource):

    def __init__(self):
        self.reqparser = reqparse.RequestParser()
        self.reqparser.add_argument('db_name', type=str, help='Name of the database')
        self.reqparser.add_argument('data', type=str, location='json')
        super(WriteData, self).__init__()

    def post(self):
        # How to read the body of the request
        args = self.reqparser.parse_args()
        # data_tbw = args['data_to_be_written']
        db_name = args['db_name']

        # The data to be written into a database
        json_data = request.get_json()

        # Right now, I can read the data from a post request
        # TODO: Write the data into a database.

        return True


api.add_resource(NewDb, '/newdb')
api.add_resource(GetDBs, '/getdbs')
api.add_resource(DeleteDB, '/deletedb')
api.add_resource(WriteData, '/writedata')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4545)