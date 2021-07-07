from flask import Flask, request, render_template, redirect, url_for, abort, session, jsonify

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.project

app = Flask(__name__)
app.secret_key = b'aaa!111/'


@app.route('/test')
def test2():
    return '로그인을 환영합니다'


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
                return redirect(url_for('form'))
        except:
            return '아이디와 패스워드 확인해주세요'
    if request.method == 'GET':
        return render_template('login.html')


# 로그인 사용자만 접근 가능으로 만들면

@app.route('/form')
def form():
    if 'userid' in session:
        return render_template('success.html')
    return redirect(url_for('login'))


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)
