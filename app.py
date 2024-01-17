import sys

from flask import Flask,request

app = Flask(__name__)

@app.route("/")
def index():
    return "旅行行き先ガチャ"

if __name__=="__main__":
    app.run()
