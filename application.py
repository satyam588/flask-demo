from flask import Flask, request
from flask_restful import Resource, Api

application = Flask(__name__)
api = Api(application)


class Index(Resource):
    def get(self):
        return {'hello': 'Get Method'}

    def post(self):
        json_request = request.get_json()
        return json_request


class Param(Resource):
    def get(self, num, num2):
        response = {
            'message': 'Multiplication of Inputs',
            'status': 1,
            'response': num*num2
        }
        return response


# Routes
api.add_resource(Index, '/')
api.add_resource(Param, '/param/<int:num>/<int:num2>')


if __name__ == "__main__":
    application.run(debug=True)
