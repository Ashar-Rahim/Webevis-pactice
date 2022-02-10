
from flask import Flask, request, jsonify, send_file
import os
from PIL import Image, ImageFilter
from werkzeug.utils import secure_filename
from PIL import ImageEnhance
import gunicorn
import sys

app = Flask(__name__)

app.secret_key = "Shary_coder_1925"

UPLOAD_FOLDER = 'static\\img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def image_filtering(img, fil):
    img = Image.open(str(img))
    if fil == 'BLUR':
        filter_image = img.filter(ImageFilter.BLUR)
    elif fil == 'EMBOSS':
        filter_image = img.filter(ImageFilter.EMBOSS)
    elif fil == 'CONTOUR':
        filter_image = img.filter(ImageFilter.CONTOUR)
    elif fil == 'DETAIL':
        filter_image = img.filter(ImageFilter.DETAIL)
    elif fil == 'EDGE_ENHANCE':
        filter_image = img.filter(ImageFilter.EDGE_ENHANCE)
    elif fil == 'EDGE_ENHANCE_MORE':
        filter_image = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    elif fil == 'FIND_EDGES':
        filter_image = img.filter(ImageFilter.FIND_EDGES)
    else:
        filter_image = img
    return filter_image


@app.route('/')
def main():
    return 'Homepage'


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')
    fil = request.form.get('fil')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            success = True

        else:
            errors[file.filename] = 'File type is not allowed'

    if success and errors:
        errors['message'] = 'File(s) successfully uploaded'
        resp = jsonify(errors)
        resp.status_code = 500
        return resp
    if success:
        resp = jsonify({'message': 'Files successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


if __name__ == '__main__':
    app.run(debug=True)

