import os
from datetime import datetime
from flask import Flask, request, render_template

from main import infer_by_web

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # Project abs path


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload_page", methods=["GET"])
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'static/')
    if not os.path.isdir(target):
        os.mkdir(target)
        
    option = request.form.get('optionsPrediction')

    for upload in request.files.getlist("file"):
        filename = upload.filename
        ext = os.path.splitext(filename)[1]
        if ext.lower() not in [".jpg", ".png"]:
            return render_template("Error.html", message="Files uploaded are not supported...")
        
        savefname = datetime.now().strftime('%Y-%m-%d_%H_%M_%S') + ext
        destination = os.path.join(target, savefname)
        upload.save(destination)
        result = predict_image(destination, option)
        print("Prediction: ", result)
    
    return render_template("complete.html", image_name=savefname, result=result)


def predict_image(path, type):
    return infer_by_web(path, type)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True, use_reloader=False)

