from flask import Flask, request
from flask_restful import Resource, Api
import os
import random
import string
from PIL import Image
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfMerger
import shutil

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
                    convertedFilename = ''.join(random.choice(string.ascii_lowercase + string.digits)
                                                for _ in range(10))
                    convertedPath = "uploads/converted/"+convertedFilename + \
                        "."+request.form['to_format']

                    img = Image.open(savePath)
                    # Covert RGBA to RGB
                    if fileExtention == 'webp':
                        img = img.convert('RGB')

                    img.save(convertedPath)

                    message = 'Conversion Success!'
                    data = {
                        'filename': file.filename,
                        'size': size,
                        'from_format': fileExtention,
                        'to_format': request.form['to_format'],
                        'save_path': savePath,
                        'converted_filename': convertedFilename,
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


class SplitPdf(Resource):
    def post(self):
        file = request.files["pdf"]

        if file.filename != '':
            fileExtention = file.filename.split('.')
            fileExtention = fileExtention[-1]

            # Save Path
            savePath = "uploads/pdfs/" + \
                ''.join(random.choice(string.ascii_lowercase + string.digits)
                        for _ in range(10))+"."+fileExtention
            file.save(savePath)
            # Get Size in byte
            size = os.stat(savePath).st_size

            # Get Mime-type
            allowedImageType = ['pdf']

            if (size < 5000000) and (fileExtention in allowedImageType):
                # try:
                uploadedFilename = ''.join(random.choice(string.ascii_lowercase + string.digits)
                                           for _ in range(10))
                convertedPath = "uploads/pdfs/splitted/"+uploadedFilename

                inputpdf = PdfFileReader(open(savePath, "rb"))

                if not os.path.exists(convertedPath):
                    os.makedirs(convertedPath)

                for i in range(inputpdf.numPages):
                    output = PdfFileWriter()
                    if (request.form['extract'] == 'page') and (request.form['page'] != ''):
                        pageList = request.form['page'].split(',')
                        if str(i + 1) in pageList:
                            i = i + 1
                        if str(i) in pageList:
                            print(i)
                            output.addPage(inputpdf.getPage(i-1))
                            with open(convertedPath+"/"+uploadedFilename+"_page_"+str(i)+".pdf", "wb") as outputStream:
                                output.write(outputStream)

                    elif (request.form['extract'] == 'range') and (request.form['range'] != ''):
                        pageRange = request.form['range'].split('-')

                        if int(pageRange[1]) == inputpdf.numPages:
                            i = i + 1

                        if (i >= int(pageRange[0])) and (i <= int(pageRange[1])):
                            output.addPage(inputpdf.getPage(i-1))
                            with open(convertedPath+"/"+uploadedFilename+"_page_"+str(i)+".pdf", "wb") as outputStream:
                                output.write(outputStream)

                    else:
                        output.addPage(inputpdf.getPage(i))
                        with open(convertedPath+"/"+uploadedFilename+"_page_"+str(i+1)+".pdf", "wb") as outputStream:
                            output.write(outputStream)

                shutil.make_archive(
                    "uploads/pdfs/splitted/"+uploadedFilename, "zip", convertedPath)
                shutil.rmtree(convertedPath, ignore_errors=True)
                message = 'Conversion Success!'
                data = {
                    'filename': file.filename,
                    'size': size,
                    'from_format': fileExtention,
                    'save_path': savePath,
                    'converted_filename': uploadedFilename,
                    'zip_file': convertedPath+'.zip'
                }
                # except:
                #     message = 'Something went Wrong, Please try again!'
                #     data = []

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
                    'message': 'Only PDF file and Less then 2MB allowed!',
                    'status': 0,
                    'data': []
                }
                return response
        else:
            response = {
                'message': 'Pdf file is Required!',
                'status': 0,
                'data': []
            }
            return response


class MergePdf(Resource):
    def post(self):
        files = request.files.getlist("pdfs[]")

        data = []
        for file in files:
            data.append(file.filename)
        return data
        folderName = ''.join(random.choice(string.ascii_lowercase + string.digits)
                             for _ in range(10))
        uploadLocation = "uploads/pdfs/merge/"+folderName
        if not os.path.exists(uploadLocation):
            os.makedirs(uploadLocation)
        # savePath = "uploads/" + \
        #     ''.join(random.choice(string.ascii_lowercase + string.digits)
        #             for _ in range(10))+"."+fileExtention
        count = 1
        allFileName = []

        # return uploadLocation
        for file in files:
            if file.filename != '':
                fileExtention = file.filename.split('.')
                fileExtention = fileExtention[-1]
                savePath = uploadLocation+"/"+str(count)+"."+fileExtention
                file.save(savePath)
                # Get Size in byte
                size = os.stat(savePath).st_size

                # Get Mime-type
                allowedImageType = ['pdf']

                if (size < 5000000) and (fileExtention in allowedImageType):
                    allFileName.append(str(count)+"."+fileExtention)
                    # try:
                    uploadedFilename = ''.join(random.choice(string.ascii_lowercase + string.digits)
                                               for _ in range(10))
                    convertedPath = "uploads/pdfs/splitted/"+uploadedFilename

                    message = 'Merged Success!'
                    data = {
                        'filename': file.filename,
                        'size': size,
                        'from_format': fileExtention,
                        'save_path': savePath,
                        'converted_filename': uploadedFilename,
                    }

                    response = {
                        'message': message,
                        'status': 1,
                        'data': data
                    }

                else:
                    if os.path.exists(savePath):
                        os.remove(savePath)
                    response = {
                        'message': 'Only PDF file and Less then 2MB allowed!',
                        'status': 0,
                        'data': []
                    }
                    return response
            else:
                response = {
                    'message': 'Pdf files are Required!',
                    'status': 0,
                    'data': []
                }
                return response
            count = count + 1

        merger = PdfMerger()

        for pdf in allFileName:
            merger.append(uploadLocation+"/"+pdf)

        resultPdf = "uploads/pdfs/merge/result/"+folderName+".pdf"
        merger.write(resultPdf)
        merger.close()

        response = {
            'message': message,
            'status': 1,
            'folder_Name': uploadLocation,
            'file_Names': allFileName,
            'result_Pdf': resultPdf,
        }
        return response


# Routes
api.add_resource(Index, '/')
api.add_resource(Param, '/param/<int:num>/<int:num2>')
api.add_resource(Upload, '/upload')
api.add_resource(SplitPdf, '/split-pdf')
api.add_resource(MergePdf, '/merge-pdf')


if __name__ == "__main__":
    application.run(debug=True)
