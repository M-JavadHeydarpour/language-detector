import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from detector.detector import detection

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SOURCE_CODES_PATH'] = '/tmp/flask_data'
ALLOWED_EXTENSIONS = {'rar', 'zip', 'tar.gz', 'tar'}


def allowed_file(filename):
    print(filename.rsplit('.', 1)[1].lower())
    print(filename.rsplit('.', 1)[0].lower())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/v1/sourcecode', methods=['POST'])
def get_source_code():
    if 'file' not in request.files:
        resp = jsonify({'message': 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message': 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['SOURCE_CODES_PATH'], filename))
        resp = jsonify({'message': 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message': 'Allowed file types are rar zip tar.gz tar'})
        resp.status_code = 400
        return resp


@app.route('api/v1/language', methods=['GET'])
def get_language():
    if request.args.get('source_code'):
        lang = detection(source_code=request.args.get('source_code'), source_path=app.config['SOURCE_CODES_PATH'])
        resp = jsonify({'language': lang})
        resp.status_code = 200
        return resp
    elif not request.args.get('source_code'):
        resp = jsonify({'message': 'No source code defined'})
        resp.status_code = 400
        return resp
    else:
        resp = jsonify({'message': 'Not Found'})
        resp.status_code = 404
        return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
