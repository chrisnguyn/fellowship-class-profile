import json

from data_collection.contribution_chart import get_contribution_chart
from data_collection.followers_following import get_followers_following
from data_collection.code_review_by_user import get_num_issue_comments, get_num_pr_reviews
from data_collection.commit_stats import get_commit_stats
from data_collection.issues import get_issues
from data_collection.most_active_day import calculate_max
from data_collection.most_worked_with import get_people_worked_with
from data_collection.most_worked_on import get_most_worked_on
from data_collection.org_repo_stats import get_all_original_repos_in_MLH, get_all_forked_repos_in_MLH
from data_collection.group_members_by_teams import get_members_by_teams

from web.app import db
from web.models import UserInfo, Repository


def store_mlh_user_data():
    team_list = get_members_by_teams()
    for team_name, members in team_list.items():
        if "pod" or "mentors" or "staff" in team_name:
            for member in members:
                add_new_user(member, team_name)
    db.session.commit()


def store_mlh_repo_data():
    forked_repos = get_all_forked_repos_in_MLH()
    original_repos = get_all_original_repos_in_MLH()
    for repo in forked_repos:
        add_new_repo(repo)
    for repo in original_repos:
        add_new_repo(repo)

    db.session.commit()


def add_new_user(user, team_name):
    followers, following = get_followers_following(user)
    activity_stats = calculate_max(user)
    repo_stats = get_most_worked_on(user)
    total_contribution_graph = get_contribution_chart(user)
    new_user = UserInfo(
        pod=team_name,
        github_username=user,
        num_code_reviews=get_num_pr_reviews(user),
        num_issues_opened=get_issues(user),
        num_issues_contributed=get_num_issue_comments(user),
        repo_changes=json.dumps(get_commit_stats(user)),
        collaborators=json.dumps(get_people_worked_with(user)),
        num_followers=followers,
        num_following=following,
        most_active_day=json.dumps(activity_stats["max_day"]),
        most_active_week=json.dumps(activity_stats["max_week"]),
        github_id=json.dumps(repo_stats["data"]["user"]["id"]),
        most_popular_pr=json.dumps(
            repo_stats["data"]["user"]["contributionsCollection"]["popularPullRequestContribution"]),
        top_repos=json.dumps(
            repo_stats["data"]["user"]["contributionsCollection"]["pullRequestContributionsByRepository"]),
        num_prs=repo_stats["data"]["user"]["contributionsCollection"]["totalPullRequestContributions"],
        num_commits=repo_stats["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        num_repos=repo_stats["data"]["user"]["contributionsCollection"]["totalRepositoriesWithContributedPullRequests"],
        contribution_graph=total_contribution_graph
    )
    db.session.add(new_user)


def add_new_repo(repo):
    if repo["isFork"]:
        author = repo["parent"]["owner"]["login"]
    else:
        author = repo["owner"]["login"]
    
    if repo.get("primaryLanguage", False):
        lang = repo["primaryLanguage"]["name"]
    else:
        lang = "None"

    new_repo = Repository(
        repo_id=repo["id"],
        repo_name=repo["name"],
        repo_author=author,
        primary_language = lang, 
        url=repo["url"],
        is_fork=repo["isFork"],
    )
    db.session.add(new_repo)
