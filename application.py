from flask import Flask
from flask_restful import Resource, Api

application = Flask(__name__)
api = Api(application)

# @application.route("/", methods=['GET', 'POST'])
# def index():
#     return "<h1>This is OneUtils Flask Env. API</h1>"

# @application.route("/another", methods=['GET', 'POST'])
# def another():
#     return "<h1>This is OneUtils Another Page</h1>"
class Index(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(Index, '/')



if __name__ == "__main__":
    application.run(debug=True)
