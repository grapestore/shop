from flask import Flask, request, render_template, redirect, url_for, abort, session, jsonify

app = Flask(__name__)
app.secret_key = b'aaa!111/'

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://test:test@localhost', 27017)
db = client.project




# 로그인 사용자만 접근 가능으로 만들면
@app.route('/form')
def form():
    if 'userid' in session:
        return render_template('success.html')
    return redirect(url_for('login'))


##로그인시 mall
@app.route('/mall')
def mall():
    if 'userid' in session:
        return render_template('shop.html')
    return redirect(url_for('login'))


## mall list api
@app.route('/mall/list', methods=['GET'])
def mall_list():
    # 여러개 찾기 - 예시 ( _id 값은 제외하고 출력)
    all_item = list(db.item.find({}, {'_id': False}))
    return jsonify({'item': all_item})


## mall list delete
@app.route('/mall/delete', methods=['POST'])
def mall_delete():
    delete_receive = request.form['delete_give']
    # 지우기 - 예시
    db.item.delete_one({'url': delete_receive})
    return jsonify({'msg': '삭제완료'})


## add item
@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'userid' in session:
        if request.method == 'POST':
            url = request.form['url_give']
            image = request.form['img_give']
            brand = request.form['brand_give']
            category = request.form['category_give']
            price = request.form['price_give']
            # 저장
            doc = {
                'url': url,
                'image': image,
                'brand': brand,
                'category': category,
                'price': price}
            db.item.insert_one(doc)
            return jsonify({'msg': 'success'})
        if request.method == 'GET':
            return render_template('add.html')
    return redirect(url_for('login'))


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('loggedin.html')


## 회원가입을 주는 부분
@app.route('/sign', methods=['GET', 'POST'])
def sign1():
    if request.method == 'POST':
        id_receive = request.form['id_give']
        pw_receive = request.form['pw_give']
        # 저장 - 예시
        doc = {'id': id_receive, 'pw': pw_receive}
        db.UserID.insert_one(doc)
        return jsonify({'msg': 'success'})
    if request.method == 'GET':
        return render_template('signin.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        id = request.form['id_give']
        pw = request.form['pw_give']
        check_id = db.UserID.find_one({'id': id}, {'_id': False})
        try:
            if id == check_id['id'] and pw == check_id['pw']:
                session['userid'] = check_id['id']
                return redirect(url_for('mall'))
        except:
            return '아이디와 패스워드 확인해주세요'
    if request.method == 'GET':
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
