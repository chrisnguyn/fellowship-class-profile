import os

import requests

from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from web.github import GitHubExtension

app = Flask(__name__, template_folder='./templates')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = 'this-really-needs-to-be-changed'

db = SQLAlchemy(app)
github_extension = GitHubExtension()


@app.route('/')
def index():
    return render_template('index.html', email=session.get('github_user_email'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/personal')
def personal():
    return render_template('personal.html')


@app.route('/status_check')
def status_check():
    return jsonify({"success": "up"})


@app.route('/callback/github')
def callback():
    response = github_extension.get_access_token_with_auth_code(
        request.args.get('code'))

    if response.ok:
        access_token = response.json()['access_token']
        session['access_token'] = access_token

        url = GitHubExtension.API_URL + '/user'
        params = {'access_token': access_token}

        github_user_data = requests.get(url, params=params).json()
        github_user_email = requests.get(url + '/emails', params=params).json()

        session['github_user_email'] = github_user_email[0]['email']

        if not User.query.filter_by(email=session['github_user_email']).first():
            new_user = User(github_access_token=access_token,
                            github_username=github_user_data['login'],
                            email=github_user_email[0]['email'])
            db.session.add(new_user)
            db.session.commit()

        session['user_id'] = User.query.filter_by(email=session['github_user_email']).first().id

        return redirect(url_for('index'))

    return 'Internal Server Error', 500


@app.route('/login/github')
def login_github():
    return redirect('https://github.com/login/oauth/authorize?client_id'
                    '=fc7c0f9b52387b87d52d&scope=repo user:email')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    github_access_token = db.Column(db.String(100))
    github_username = db.Column(db.String(100), unique=True)

    def __init__(self, email, github_access_token, github_username):
        self.email = email
        self.github_access_token = github_access_token
        self.github_username = github_username
