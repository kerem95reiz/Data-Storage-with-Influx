from flask import Flask
from flask_restful import Resource, Api
from db import db_ops

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'Kerem',
                'sonunda': 'Sonuc aldin'}

class WriteData(Resource):
    def get(self):
        x = db_ops()
        return {'veriler' : 'yazildi'}


api.add_resource(HelloWorld, '/')
api.add_resource(WriteData, '/yaz')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4545)