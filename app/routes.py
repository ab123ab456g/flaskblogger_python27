# -*- coding: UTF-8 -*-

from flask import render_template, request, redirect, url_for

from flask import session, make_response

from datetime import datetime

from app import app
from app.controllers import *
import hashlib 

@app.route('/')
def main():
    posts = PostIt.get_all()
    posts.reverse()
    if 'uid' in session:
        if session['uid'] == request.cookies.get('uid'):
            username = request.cookies.get('username')
            return render_template('main.html', posts = posts, username=username)
    else:
        return render_template('main.html', posts = posts)

@app.route('/login')
def login():
    if 'uid' in session:
        if session['uid'] == request.cookies.get('uid'):
            return redirect('/')
    else:
        return render_template('login.html')

@app.route('/login/check', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']
    if Login.isLogin(username, password):
        uid = hashlib.sha256(username+','+str(datetime.now())).hexdigest()
        session['uid'] = uid
        resp = make_response(redirect('/'))
        resp.set_cookie("uid", uid)
        resp.set_cookie("username", username)
        return resp
    else:
        return redirect('/login/fail')

@app.route('/login/fail')
def login_fail():
    return render_template('login_fail.html')

@app.route('/logout')
def logout():
    session.clear()
    resp = make_response(render_template('logout.html'))
    resp.set_cookie('sessionID', '', expires=0)
    resp.set_cookie('uid', '', expires=0)
    resp.set_cookie('username', '', expires=0)
    return resp

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/fail')
def register_fail():
    return render_template('register_fail.html')

@app.route('/edit')
def edit():
    return render_template('edit.html')

@app.route('/editlist')
def editlist():
    return render_template('editlist.html')

@app.route('/post/<int:id>')
def post(id):
    post = PostIt.get(id)
    if post:
        return render_template('post.html', post=post)
    else:
        return 'can not find the article'