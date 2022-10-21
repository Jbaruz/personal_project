from flask import send_from_directory
from flask_base import app


@app.route('/uploads/<name>')
def download_file(name):
    print("QUIERO VER IMAGE---->", name)
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)



