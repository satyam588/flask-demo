from flask import Flask, request
from flask_restful import Resource, Api
import os
import random
import string
from PIL import Image

application = Flask(__name__, static_url_path='/uploads',
                    static_folder='uploads')
api = Api(application)


class Index(Resource):
    def get(self):
        return {'message': 'Hello this is demo API!'}


class Param(Resource):
    def get(self, num, num2):
        response = {
            'message': 'Multiplication of Inputs',
            'status': 1,
            'response': num*num2
        }
        return response


class Upload(Resource):
    def post(self):
        file = request.files["image"]
        if (file.filename != '') and (request.form['to_format'] != ''):
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
            allowedImageType = ['png', 'jpg', 'jpeg', 'bmp', 'tiff', 'webp']

            if (size < 2000000) and (fileExtention in allowedImageType):
                try:
                    convertedPath = "uploads/converted/"+''.join(random.choice(string.ascii_lowercase + string.digits)
                                                                 for _ in range(10))+"."+request.form['to_format']
                    img = Image.open(savePath)
                    img.save(convertedPath)

                    message = 'Conversion Success!'
                    data = {
                        'filename': file.filename,
                        'size': size,
                        'from_format': fileExtention,
                        'to_format': request.form['to_format'],
                        'save_path': savePath,
                        'converted_path': convertedPath
                    }
                except:
                    message = 'Error occured!'
                    data = []

                response = {
                    'message': message,
                    'status': 1,
                    'data': data
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
        else:
            response = {
                'message': 'Image and Result format is Required!',
                'status': 0,
                'data': []
            }
            return response


# Routes
api.add_resource(Index, '/')
api.add_resource(Param, '/param/<int:num>/<int:num2>')
api.add_resource(Upload, '/upload')


if __name__ == "__main__":
    application.run(debug=True)
