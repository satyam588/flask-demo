from flask import Flask, request
from flask_restful import Resource, Api

application = Flask(__name__)
api = Api(application)

class Index(Resource):
    def get(self):
        return {'hello': 'Get Method'}

    def post(self):
        return {'hello': 'Post Method'}

class Another(Resource):
    def get(self):
        return {'another': 'page'}


# Routes
api.add_resource(Index, '/')
api.add_resource(Another, '/another')



if __name__ == "__main__":
    application.run(debug=True)
