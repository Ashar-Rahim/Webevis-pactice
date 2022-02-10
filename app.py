
from flask import Flask, request, jsonify, send_file
import os
from PIL import Image, ImageFilter
from werkzeug.utils import secure_filename
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
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True

            user_image = 'static\\img\\' + filename
            new_image = image_filtering(user_image, fil)
            new_image.save("static\\img\\newData\\new_img.png")
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
        return send_file("static\\img\\newData\\new_img.png")
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


@app.route('/compress', methods=['POST'])
def compress():
    # check if the post request has the file part
    if 'files[]' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp

    files = request.files.getlist('files[]')
    qual = request.form.get('qual')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            success = True

            user_image = 'static\\img\\' + filename
            picture = Image.open(user_image)
            print(picture)

            picture.save("static\\img\\Compressed_" + filename, optimize=True, quality=int(qual))

        else:
            errors[file.filename] = 'File type is not allowed'

    if success:
        resp = jsonify({'message': 'Files successfully uploaded'})
        resp.status_code = 201
        return send_file("static\\img\\Compressed_" + filename)
    else:
        resp = jsonify(errors)
        resp.status_code = 500
        return resp


if __name__ == '__main__':
    app.run(debug=True)
