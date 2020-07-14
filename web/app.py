from flask import Flask, redirect, render_template, url_for
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/personal')
def personal():
    return render_template('personal.html')
