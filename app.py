import sys

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import random
from dotenv import load_dotenv
import os

# .envから環境変数を読み込む
load_dotenv()

# 画像読み込み
app = Flask(__name__, static_folder='./templates/images')

# DB設定
app.config['SQLALCHEMY_DATABASE_URI'] = '{db-connection}://{user}:{password}@{host}/{db-name}?charset=utf8'.format(**{
      'db-connection': os.getenv('DB_CONNECTION'),
      'user': os.getenv('DB_USER'),
      'password': os.getenv('DB_PASSWORD'),
      'host': os.getenv('DB_HOST'),
      'db-name': os.getenv('DB_NAME')
  })
db = SQLAlchemy(app)

# モデル定義
class TravelGacha(db.Model):
    __tablename__ = "travel_gachas"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    used = db.Column(db.Integer)

    def __init__(self, name, used):
            self.name = name
            self.used = used
    def __repr__(self):
        # __repr__メソッドは"print(TravelGachaインスタンス)"した時に出力する値を決めることができる。
        return "[id: %s, name: '%s', used: %s]" % (self.id, self.name, self.used)
    def createGacha(name):
        new_record = TravelGacha(name=name, used=0)
        db.session.add(new_record)
        db.session.commit()
    def updateGacha(id):
        gacha = TravelGacha.searchBy(id)
        gacha.used = 1
        db.session.commit()
    def searchBy(id):
        return db.session.query(TravelGacha)\
            .filter(TravelGacha.id == id)\
            .one()
    def getAllGachas():
        return db.session.query(TravelGacha)\
            .all()
    def getUnusedGachas():
        return db.session.query(TravelGacha)\
            .filter(TravelGacha.used == 0)\
            .all()
    def getDestination():
        destinations =  db.session.query(TravelGacha)\
            .filter(TravelGacha.used == 0)\
            .all()
        if len(destinations) > 0:
            destination = random.choice(destinations)
            TravelGacha.updateGacha(destination.id)
            return destination.name
        else:
            return ''

# ルーティング
# formの表示
@app.route("/")
def index():
    return render_template('form.html') #htmlファイルの表示

# レコードの作成
@app.route("/create", methods=["POST"])
def insert():
    TravelGacha.createGacha(request.form["name"])
    return redirect("/")

# レコードの更新
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    TravelGacha.updateGacha(id)

# 全レコード取得
@app.route("/get-all", methods=["GET"])
def  select():
    return str(TravelGacha.getAllGachas())

# 個別レコード取得
@app.route('/get/<int:id>', methods=['GET'])
def getGacha(id):
    return str(TravelGacha.searchBy(id))

# 目的地の名前取得
@app.route("/destination", methods=["GET"])
def get_destination():
    destination_name = TravelGacha.getDestination()
    if destination_name == '':
        return render_template('error.html')
    else:
        return render_template('destination.html', destination=destination_name) #htmlファイルの表示

# 再度ガチャ
@app.route("/retry")
def retry():
    return render_template('form.html') #htmlファイルの表示

if __name__=="__main__":
    app.run()
