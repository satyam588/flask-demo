from flask import Flask, request
from flask_restful import Resource, Api

application = Flask(__name__)
api = Api(application)


class Index(Resource):
    def get(self):
        return {'hello': 'Get Method'}

    def post(self):
        return {'hello': 'Post Method'}

class Param(Resource):
    def get(self, num, num2):
        return {'pram value multiply': num*num2}


# Routes
api.add_resource(Index, '/')
api.add_resource(Param, '/param/<int:num>/<int:num2>')


if __name__ == "__main__":
    application.run(debug=True)
