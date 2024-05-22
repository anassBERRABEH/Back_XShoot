from flask import request, jsonify, send_file
from config import app, db
from models import Event
import os
# this was aded too
from flask import jsonify
from fun import process_folder
import json
from zipfile import ZipFile
import io

# add for images:
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# end here ----------------------------------
# added for images:
@app.route("/addEvent", methods=["POST"])
def upload_images():
    name = request.form['name']

    if 'files' not in request.files:
        return jsonify({"error": "No files part"}), 400

    files = request.files.getlist('files')

    if not files or any(file.filename == '' for file in files):
        return jsonify({"error": "No selected files"}), 400

    image_paths = []
    os.mkdir(app.config['UPLOAD_FOLDER'] + '/' + name)
    for file in files:
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + name, filename)
        file.save(file_path)
        image_paths.append(file_path)

    new_envent = Event(
        name=name,
        folder=app.config['UPLOAD_FOLDER'] + '/' + name
    )
    db.session.add(new_envent)
    db.session.commit()

    process_folder(app.config['UPLOAD_FOLDER'] + '/' + name)

    return jsonify({"message": "Files uploaded successfully"}), 201


@app.route('/list_images/<filename>/<bibN>', methods=["GET"])
def list_images(filename, bibN):
    with open(app.config['UPLOAD_FOLDER'] + "/" + filename + '/bib_images.json', 'r') as json_file:
        data = json.load(json_file)
    if bibN not in data:
        return jsonify({"images": []})

    # images = []
    # for filename in os.listdir(app.config['UPLOAD_FOLDER']):
    #     if filename.endswith(('.png', '.jpg', '.jpeg')):
    #         images.append(filename)
    return jsonify({"images": data[bibN]})

@app.route('/download_image/<filename>/<img>', methods=["GET"])
def download_image(filename, img):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'] + "/" + filename, img)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/download_all_images/<name>/<bibN>', methods=["GET"])
def download_all_images(name, bibN):
    with open(app.config['UPLOAD_FOLDER'] + "/" + name + '/bib_images.json', 'r') as json_file:
        data = json.load(json_file)
    if bibN not in data:
        a = []
    a = data[bibN]

    memory_file = io.BytesIO()
    upload_folder = app.config['UPLOAD_FOLDER']
    directory_path = os.path.join(upload_folder, name)

    with ZipFile(memory_file, 'w') as zf:
        for file in a:
            zf.write(file, os.path.relpath(file, directory_path))

    memory_file.seek(0)
    return send_file(memory_file, download_name='images.zip', as_attachment=True)

@app.route("/events", methods=["GET"])
def get_events():
    events = Event.query.all()
    json_events = list(map(lambda x: x.to_json(), events))
    return jsonify({"events": json_events})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
