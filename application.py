from flask import Flask

application = Flask(__name__)

@application.route("/", methods=['GET', 'POST'])
def index():
    return "<h1>This is OneUtils Flask Env. API</h1>"

@application.route("/another", methods=['GET', 'POST'])
def another():
    return "<h1>This is OneUtils Another Page</h1>"



if __name__ == "__main__":
    application.run()
