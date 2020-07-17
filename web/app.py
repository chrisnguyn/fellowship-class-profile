import requests

from flask import jsonify, render_template, request, session, redirect, url_for, Blueprint, json

from web.factory import db
from web.github import GitHubExtension
from web.models import User, UserInfo, GlobalStats

bp = Blueprint('app', __name__)

github_extension = GitHubExtension()


@bp.route('/')
def index():
    return render_template('index.html', email=session.get('github_user_email'))


@bp.route('/user_stats')
def get_user_stats():
    username = request.args.get('username')
    if username:
        user = UserInfo.query.filter_by(github_username=username).first()
        if user:
            return jsonify({
                "github_username": user.github_username,
                "github_id": user.github_id,
                "pod": user.pod,
                "num_code_reviews": user.num_code_reviews,
                "num_issues_opened": user.num_issues_opened,
                "num_issues_contributed": user.num_issues_contributed,
                "repo_changes": json.loads(user.repo_changes),
                "collaborators": json.loads(user.collaborators),
                "num_followers": user.num_followers,
                "num_following": user.num_following,
                "most_active_day": json.loads(user.most_active_day),
                "most_active_week": json.loads(user.most_active_week),
                "most_popular_pr": json.loads(user.most_popular_pr),
                "top_repos": json.loads(user.top_repos),
                "num_prs": user.num_prs,
                "num_commits": user.num_commits,
                "num_repos": user.num_repos,
                "contribution_graph": json.loads(user.contribution_graph),
            })
        else:
            return jsonify({"error": "User not found"})

    return jsonify({"error": "Username not specified"}), 400


@bp.route('/global_stats')
def get_global_stats():
    stats = GlobalStats.query.first()
    if stats:
        return jsonify({
            "repo_lang_stats": json.loads(stats.repo_lang_stats),
            "num_repos": stats.num_repos,
            "num_standups": stats.num_standups,
            "num_countries": stats.num_countries,
            "num_timezone": stats.num_timezone,
            "num_members": stats.num_members,
            "num_pods": stats.num_pods,
            "num_contributions_by_day": json.loads(stats.num_contributions_by_day),
            "num_prs": stats.num_prs,
            "num_issues_opened": stats.num_issues_opened,
            "num_issues_contributed": stats.num_issues_contributed,
            "num_commits": stats.num_commits,
            "num_code_reviews": stats.num_code_reviews,
            "num_lines_code_added_per_repo": json.loads(stats.num_lines_code_added_per_repo),
            "num_lines_code_deleted_per_repo": json.loads(stats.num_lines_code_deleted_per_repo),
            "num_files_changed_per_repo": json.loads(stats.num_files_changed_per_repo),
            "num_commits_per_repo": json.loads(stats.num_commits_per_repo),
        })
    else:
        return jsonify({"error": "Global statistics not found"})


@bp.route('/login')
def login():
    if session.get('access_token'):
        return redirect(url_for('app.personal'))
    return render_template('login.html')


@bp.route('/personal')
def personal():
    if not session.get('access_token'):
        redirect(url_for('app.login'))
    return render_template('personal.html', username=session.get('username'))


@bp.route('/status_check')
def status_check():
    return jsonify({"success": "up"})


@bp.route('/callback/github')
def callback():
    try:
        response = github_extension.get_access_token_with_auth_code(
            request.args.get('code'))

        print(response.status_code)
        print(response.text)

        access_token = response.json()['access_token']
        session['access_token'] = access_token

        url = GitHubExtension.API_URL + '/user'
        params = {'access_token': access_token}

        github_user_data = requests.get(url, params=params).json()
        github_user_email = requests.get(url + '/emails', params=params).json()

        session['github_user_email'] = github_user_email[0]['email']
        session['username'] = github_user_data['login']

        if not User.query.filter_by(email=session['github_user_email']).first():
            new_user = User(github_access_token=access_token,
                            github_username=github_user_data['login'],
                            email=github_user_email[0]['email'])
            db.session.add(new_user)
            db.session.commit()

        session['user_id'] = User.query.filter_by(email=session['github_user_email']).first().id

        return redirect(url_for('app.index'))
    except Exception as e:
        print(e)
        return 'Internal Server Error', 500


@bp.route('/login/github')
def login_github():
    return redirect('https://github.com/login/oauth/authorize?client_id'
                    '=fc7c0f9b52387b87d52d&scope=repo user:email')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('app.index'))


@bp.route('/500')
def error():
    return "Internal server error", 500



