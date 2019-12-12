#!/usr/bin/python3
from flask import Flask, render_template, request
from werkzeug import secure_filename
import flask_client as client
import os, time

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("front_end.html")

def get_file_info():
    imgName = os.listdir("./static/img")

    imgSize = []
    timeAdded = []
    for name in imgName:
        path = "./static/img/" + name
        imgSize.append(os.stat(path).st_size)
        timeAdded.append(time.ctime(os.path.getmtime(path)))
    
    imgProcessedName = os.listdir("./static/img_processed")
    txtName = os.listdir("./static/text")

    if (len(imgProcessedName) < len(imgName)):
        for i in range(len(imgName) - len(imgProcessedName)):
            imgProcessedName.append("empty")
            txtName.append("empty")

    result = []
    for name, size, time_m, name_processed, name_txt in zip(
        imgName, imgSize, timeAdded, imgProcessedName, txtName):
        result.append({'name':name, 'size':size, 'time':time_m,
                        'name_processed': name_processed, 
                        'name_txt': name_txt})

    return result


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        f = request.files['file']
        filePath = "./static/img/" + secure_filename(f.filename)
        f.save(filePath)

        files = get_file_info()

        return render_template("upload.html", files = files)
    else:
        files = get_file_info()

        return render_template("upload.html", files = files)

@app.route("/upload/process/<filename>")
def start_process(filename):
    files = get_file_info()

    processed_name = filename.split(".")[0] + "_thresh.jpg"
    if processed_name in os.listdir("./static/img_processed"):
        return render_template("upload.html", files = files)
    else:
        client.send_img(filename)
        return render_template("upload.html", files = files)

@app.route("/upload/img/<filename>")
def show_img(filename):
    filepath = "img/" + filename
    return render_template("img_static.html", filename = filepath)

@app.route("/upload/img_processed/<filename>")
def show_img_processed(filename):
    if filename == "empty":
        return render_template("empty.html")
    else:    
        filepath = "img_processed/" + filename
        return render_template("img_static.html", filename = filepath)

@app.route("/upload/text/<filename>")
def show_txt(filename):
    if filename == "empty":
        return render_template("empty.html")
    else:
        filepath = "./static/text/" + filename
        text = open(filepath, "r", encoding="utf-8")
        content = text.read()
        text.close()
        return render_template("text_static.html", text = content)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")