import requests

from flask import jsonify, render_template, request, session, redirect, url_for, Blueprint

from web.factory import db
from web.github import GitHubExtension
from web.models import User

bp = Blueprint('app', __name__)

github_extension = GitHubExtension()


@bp.route('/')
def index():
    return render_template('index.html', email=session.get('github_user_email'))


@bp.route('/login')
def login():
    return render_template('login.html')


@bp.route('/personal')
def personal():
    return render_template('personal.html')


@bp.route('/status_check')
def status_check():
    return jsonify({"success": "up"})


@bp.route('/callback/github')
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


@bp.route('/login/github')
def login_github():
    return redirect('https://github.com/login/oauth/authorize?client_id'
                    '=fc7c0f9b52387b87d52d&scope=repo user:email')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


