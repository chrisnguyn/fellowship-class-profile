import json

from followers_following import get_followers_following
from code_review_by_user import get_num_issue_comments, get_num_pr_reviews
from commit_stats import get_commit_stats
from issues import get_issues
from most_active_day import calculate_max
from most_worked_with import get_people_worked_with
from most_worked_on import get_most_worked_on, get_repos_in_MLH_project_list
from org_repo_stats import get_all_original_repos_in_MLH, get_all_forked_repos_in_MLH
from group_members_by_teams import get_members_by_teams

from web.app import db
from web.db_classes import UserInfo, Repository


class User:
    def __init__(self, user):
        self.user_name = user
        self.num_code_reviews: get_num_pr_reviews(user)
        self.num_issues_opened = get_issues(user)
        self.num_issues_contributed = get_num_issue_comments(user)
        self.repo_changes = get_commit_stats(user)
        self.collaborators = get_people_worked_with(user)

        followers, following = get_followers_following(user)
        self.num_followers = followers
        self.num_following = following

        activity_stats = calculate_max(user)
        self.most_active_day = activity_stats["max_day"]
        self.most_active_week = activity_stats["max_week"]

        repo_stats = get_most_worked_on(user)
        self.user_id = repo_stats["data"]["user"]["id"]
        self.most_popular_pr = repo_stats["data"]["user"]["contributionsCollection"]["popularPullRequestContribution"]
        self.top_repos = repo_stats["data"]["user"]["contributionsCollection"]["pullRequestContributionsByRepository"]
        self.num_prs = repo_stats["data"]["user"]["contributionsCollection"]["totalPullRequestContributions"]
        self.num_commits = repo_stats["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        self.num_repos = repo_stats["data"]["user"]["contributionsCollection"]["totalRepositoriesWithContributedPullRequests"]


def store_mlh_user_data():
    team_list = get_members_by_teams()
    for team_name, members in team_list.items():
        if "pod" or "mentors" or "staff" in team_name:
            for member in members:
                add_new_user(member)
    db.session.commit()


def store_mlh_repo_data():
    forked_repos = get_all_forked_repos_in_MLH()
    original_repos = get_all_original_repos_in_MLH()
    for repo in forked_repos:
        add_new_repo(repo)
    for repo in original_repos:
        add_new_repo(repo)

    db.session.commit()


def add_new_user(user):
    followers, following = get_followers_following(user)
    activity_stats = calculate_max(user)
    repo_stats = get_most_worked_on(user)
    new_user = UserInfo(
        user_name=user,
        num_code_reviews=get_num_pr_reviews(user),
        num_issues_opened=get_issues(user),
        num_issues_contributed=get_num_issue_comments(user),
        repo_changes=get_commit_stats(user),
        collaborators=get_people_worked_with(user),
        num_followers=followers,
        num_following=following,
        most_active_day=json.dumps(activity_stats["max_day"]),
        most_active_week=json.dumps(activity_stats["max_week"]),
        user_id=json.dumps(repo_stats["data"]["user"]["id"]),
        most_popular_pr=json.dumps(
            repo_stats["data"]["user"]["contributionsCollection"]["popularPullRequestContribution"]),
        top_repos=json.dumps(
            repo_stats["data"]["user"]["contributionsCollection"]["pullRequestContributionsByRepository"]),
        num_prs=repo_stats["data"]["user"]["contributionsCollection"]["totalPullRequestContributions"],
        num_commits=repo_stats["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"],
        num_repos=repo_stats["data"]["user"]["contributionsCollection"]["totalRepositoriesWithContributedPullRequests"],
    )
    db.session.add(new_user)


def add_new_repo(repo):
    if repo["isFork"]:
        author = repo["parent"]["owner"]["login"]
    else:
        author = repo["owner"]["login"]

    new_repo = Repository(
        repo_id=repo["id"],
        repo_name=repo["name"],
        repo_author=parent,
        primary_language=repo["primaryLanguage"]["name"],
        url=repo["url"],
        is_fork=repo["isFork"],
    )
    db.session.add(new_repo)
