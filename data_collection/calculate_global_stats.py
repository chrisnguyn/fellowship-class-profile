import json
from sqlalchemy.sql import select, func

from data_collection.org_repo_stats import get_top_languages, get_all_forked_repos_in_MLH
from web.factory import db
from web.models import GlobalStats, UserInfo, Repository


def calculate_per_repo_stats():
    commits_per_repo = {}
    lines_added_per_repo = {}
    lines_deleted_per_repo = {}
    files_changed_per_repo = {}

    # select repo_changes from userinfo
    users_repo_stats = db.session.query(UserInfo.repo_changes).all()
    for user_repo_stats in users_repo_stats:
        user_repo_stats = json.loads(user_repo_stats[0])
        for repo_name, stats in user_repo_stats.items():
            if repo_name in commits_per_repo:
                commits_per_repo[repo_name] += stats["commits"]
                lines_added_per_repo[repo_name] += stats["additions"]
                lines_deleted_per_repo[repo_name] += stats["deletions"]
                files_changed_per_repo[repo_name] += stats["changed_files"]
            else:
                commits_per_repo[repo_name] = stats["commits"]
                lines_added_per_repo[repo_name] = stats["additions"]
                lines_deleted_per_repo[repo_name] = stats["deletions"]
                files_changed_per_repo[repo_name] = stats["changed_files"]
    
    return commits_per_repo, lines_added_per_repo, lines_deleted_per_repo, files_changed_per_repo

def aggregate_per_day_contributions():
    users_daily_contributions = db.session.query(
        UserInfo).select(columns="repo_changes")

def create_new_global_stat():
    commits, added, deleted, changed = calculate_per_repo_stats()
    stats = GlobalStats(
        id=1,
        repo_lang_stats=json.dumps(
            get_top_languages(get_all_forked_repos_in_MLH())),
        num_repos=db.session.query(Repository).count(),
        num_standups=61,
        num_countries=23,
        num_timezone=15,
        num_members=db.session.query(UserInfo).count(),
        num_pods=15,
        num_commits_per_repo=json.dumps(commits),
        # num_contributions_by_day=,
        num_prs=db.session.query(func.sum(UserInfo.num_prs)),
        num_issues_contributed=db.session.query(func.sum(UserInfo.num_issues_contributed)),
        num_issues_opened=db.session.query(func.sum(UserInfo.num_issues_opened)),
        num_commits=db.session.query(func.sum(UserInfo.num_commits)),
        num_code_reviews=db.session.query(func.sum(UserInfo.num_code_reviews)),
        num_lines_code_added_per_repo=json.dumps(added),
        num_lines_code_deleted_per_repo=json.dumps(deleted),
        num_files_changed_per_repo=json.dumps(changed),
    )
    db.session.add(stats)
    db.session.commit()