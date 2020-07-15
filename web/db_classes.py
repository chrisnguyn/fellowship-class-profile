from app import db


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


class UserInfo(db.Model):
    __tablename__ = "users_info"

    user_id = db.Column(db.Integer, primary_key=True)
    pod = db.Column(db.String(120), unique=True)
    num_code_reviews = db.Column(db.Integer, unique=True)
    num_issues_opened = db.Column(db.Integer, unique=True)
    num_issues_contributed = db.Column(db.Integer, unique=True)
    repo_changes = db.Column(db.String(120), unique=True)
    collaborators = db.Column(db.String(120), unique=True)
    num_followers = db.Column(db.Integer, unique=True)
    num_following = db.Column(db.Integer, unique=True)
    most_active_day = db.Column(db.String(120), unique=True)
    most_active_week = db.Column(db.String(120), unique=True)
    most_popular_pr = db.Column(db.String(120), unique=True)
    top_repos = db.Column(db.String(120), unique=True)
    num_prs = db.Column(db.Integer, unique=True)
    num_commits = db.Column(db.Integer, unique=True)
    num_repos = db.Column(db.Integer, unique=True)


class Repository(db.Model):
    __tablename__ = "repositories"

    repo_id = db.Column(db.Integer, primary_key=True)
    repo_name = db.Column(db.String(120), unique=True)
    repo_author = db.Column(db.String(100), unique=True)
    primary_language = db.Column(db.String(100))
    is_fork = db.Column(db.Boolean)
