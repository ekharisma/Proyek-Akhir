from logging import error
from flask import Flask, request, jsonify
from services.LocationService import LocationService
import os

app = Flask(__name__)


@app.route("/")
def index():
    welcome = {"message": "Hello world"}
    return jsonify(welcome)


@app.route("/classification/csv", methods=['POST'])
def upload_csv():
    if request.files:
        uploaded_file = request.files['filename']
        file_path = os.path.join(app.config['FILE_UPLOAD'],
                                 uploaded_file.filename)
        uploaded_file.save(file_path)
        return jsonify({'message': 'success'})


@app.route("/location", methods=['POST'])
def location():
    ip: str = request.json['ip']
    location = LocationService()
    location.set_ip(ip)
    location.set_location_by_ip()
    result: dict[str:str] = location.get_map_location()
    return jsonify({
        'mesage' : result
    })


if __name__ == "__main__":
    app.config['FILE_UPLOAD'] = os.getcwd() + "/uploads/"
    app.debug = True
    if not os.path.isdir(app.config['FILE_UPLOAD']):
        raise RuntimeError("Upload path does not exist")
    app.run()