from flask import Flask, request, jsonify
import os
import extcolors
from math import sqrt
from flask_cors import CORS

UPLOAD_FOLDER = 'uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
cors = CORS(app)

app.secret_key = 'secret_key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def take_image_path(img):
    #converted_img = PIL.Image.open(img)
    col, count = extcolors.extract_from_path(img)
    list_c = [x[0] for x in col]
    dominant = list_c[0]
    r, g, b = dominant
    if (b > r) and (b > g):
        return str(dominant)
    else:
        return 'Less Solution Level can be foudnd'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# posting image


@app.route('/', methods=['POST'])
def dominant_rgb():
    # uploading the file:
    # check if the file exist
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    file = request.files['file']
    # check if the file is null
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp

    # provided the file exist, detect the dominant color
    if file and allowed_file(file.filename):
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        print('uploads/' + file.filename)

        if type(take_image_path('uploads/' + file.filename)) == type(''):
            resp = jsonify(
                {'message': take_image_path('uploads/' + file.filename)})
            resp.status_code = 201
            os.remove('uploads/' + file.filename)
            return resp

        else:
            resp = jsonify({'message': 'An error occured!'})
            resp.status_code = 201
            os.remove('uploads/' + file.filename)
            return resp

    else:
        resp = jsonify({'message': 'Something went wrong'})
        resp.status_code = 400
        os.remove('uploads/' + file.filename)
        return resp


if __name__ == "__main__":
    app.run(debug=True)
