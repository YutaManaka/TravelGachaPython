import sys

from flask import Flask, render_template

app = Flask(__name__, static_folder='./templates/images')

@app.route("/")
def index():
    return render_template('index.html') #htmlファイルの表示

if __name__=="__main__":
    app.run()
