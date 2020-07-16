from web.factory import db


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

    github_username = db.Column(db.String(120), primary_key=True)
    github_id = db.Column(db.String(120), unique=True)
    pod = db.Column(db.String(120))
    num_code_reviews = db.Column(db.Integer)
    num_issues_opened = db.Column(db.Integer)
    num_issues_contributed = db.Column(db.Integer)
    repo_changes = db.Column(db.Text)
    collaborators = db.Column(db.Text)
    num_followers = db.Column(db.Integer)
    num_following = db.Column(db.Integer)
    most_active_day = db.Column(db.String(120))
    most_active_week = db.Column(db.String(120))
    most_popular_pr = db.Column(db.Text)
    top_repos = db.Column(db.Text)
    num_prs = db.Column(db.Integer)
    num_commits = db.Column(db.Integer)
    num_repos = db.Column(db.Integer)
    contribution_graph = db.Column(db.Text)
    last_updated = db.Column(db.DateTime)


class Repository(db.Model):
    __tablename__ = "repositories"

    repo_id = db.Column(db.String(120), primary_key=True)
    repo_name = db.Column(db.String(120), unique=True)
    repo_author = db.Column(db.String(120))
    primary_language = db.Column(db.String(120))
    url = db.Column(db.String(120))
    is_fork = db.Column(db.Boolean)


class GlobalStats(db.Model):
    __tablename__ = "global_stats"

    id = db.Column(db.Integer, primary_key=True)
    repo_lang_stats = db.Column(db.Text)
    num_repos = db.Column(db.Integer)
    num_standups = db.Column(db.Integer)
    num_countries = db.Column(db.Integer)
    num_timezone = db.Column(db.Integer)
    num_members = db.Column(db.Integer)
    num_pods = db.Column(db.Integer)
    num_contributions_by_day = db.Column(db.Text)
    num_prs = db.Column(db.Integer)
    num_issues_opened = db.Column(db.Integer)
    num_issues_contributed = db.Column(db.Integer)
    num_commits = db.Column(db.Integer)
    num_code_reviews = db.Column(db.Text)
    num_lines_code_added_per_repo = db.Column(db.Text)
    num_lines_code_deleted_per_repo = db.Column(db.Text)
    num_files_changed_per_repo = db.Column(db.Text)
    num_commits_per_repo = db.Column(db.Text)
    last_updated = db.Column(db.DateTime)
