from flask import Flask

application = Flask(__name__)

@application.route("/", methods=['GET', 'POST'])
def index():
    return "<h1>Hello, Welcome to Flask!</h1>"



if __name__ == "__main__":
    application.run()
