from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import os
import random
import string
import magic

application = Flask(__name__)
api = Api(application)


class Index(Resource):
    def get(self):
        return {'hello': 'Get Method'}

    def post(self):
        file = request.files["image"]
        if file.filename != '':
            fileExtention = file.filename.split('.')
            fileExtention = fileExtention[-1]

            # Save Path
            savePath = "uploads/" + \
                ''.join(random.choice(string.ascii_lowercase + string.digits)
                        for _ in range(10))+"."+fileExtention
            file.save(savePath)
            # Get Size in byte
            size = os.stat(savePath).st_size

            # Get Mime-type
            mimeType = magic.from_file(savePath, mime=True)

            if (size < 2000000) and ('image' in mimeType):
                response = {
                    'filename': file.filename,
                    'size': size,
                    'extention': fileExtention,
                    'save_path': savePath,
                    'mimeitype': mimeType
                }
                return response
            else:
                if os.path.exists(savePath):
                    os.remove(savePath)
                response = {
                    'message': 'Only Image and Less then 2MB file allowed!',
                    'status': 0,
                    'data': []
                }
                return response


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
