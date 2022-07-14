import os
from cv2 import FileStorage_NAME_EXPECTED
from flask import Flask,render_template, request
from datetime import datetime
import getCompScore
import cv2


app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = "./static/Upload"

@app.route("/",methods=['GET'])
def func():
    return render_template("index.html")

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            # print(image.filename)
            # print(type(image.filename))
            image.save(os.path.join(app.config["IMAGE_UPLOADS"], image.filename))
            filename = os.path.join(app.config["IMAGE_UPLOADS"], image.filename)
            im=cv2.imread(filename)
            res=getCompScore.score(im)
            # print(filename)
            return render_template("score.html",ROT=res[0],DIAGONAL=res[1],VISUAL_BALANCE=res[2],OBJECT_SIZE=res[3],TOTAL=res[4],FINAL=res[5],IMAGE_PATH=filename)



if __name__=="__main__":
    app.run(debug=True,port=8000)


