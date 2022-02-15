from flask import Flask, request, jsonify, send_file
from PIL import Image, ImageFilter
from werkzeug.utils import secure_filename
from PIL import ImageEnhance
import gunicorn
import sys

app = Flask(__name__)

app.secret_key = "Shary_coder_1925"

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
    elif fil == 'SHARPEN':
        filter_image = img.filter(ImageFilter.SHARPEN)
    elif fil == 'BRIGHTER':
        filter_image = img.filter(ImageFilter.MaxFilter(size=3))
    elif fil == 'DARKER':
        filter_image = img.filter(ImageFilter.MinFilter(size=3))
    elif fil == 'SMOOTH':
        filter_image = img.filter(ImageFilter.SMOOTH)
    elif fil == 'SMOOTH_MORE':
        filter_image = img.filter(ImageFilter.SMOOTH_MORE)
    elif fil == 'G_BLUR':
        filter_image = img.filter(ImageFilter.GaussianBlur)
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
    compress = request.form.get('compress')
    quality = request.form.get('quality')

    errors = {}
    success = False

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(filename)

            user_image = filename
            new_image = image_filtering(user_image, fil)
            if compress == 'true':
                rgb_img = new_image.convert('RGB')
                rgb_img.save("filtered_img.jpg",
                               optimize=True,
                               quality=int(quality))
                pass
            else:
                new_image.save("filtered_img.jpg")

            success = True

            if success:
                resp = jsonify({'message': 'Files successfully uploaded'})
                resp.status_code = 201

                return send_file("filtered_img.jpg")
            else:
                resp = jsonify(errors)
                resp.status_code = 500
                return resp

        else:
            errors[file.filename] = 'File type is not allowed'


if __name__ == '__main__':
    app.run(debug=True)
