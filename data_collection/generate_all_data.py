from followers_following import get_followers_following
from code_review_by_user import get_num_issue_comments, get_num_pr_reviews
from commit_stats import get_commit_stats
from issues import get_issues
from most_active_day import calculate_max
from most_worked_with import get_people_worked_with
from most_worked_on import get_most_worked_on, get_repos_in_MLH_project_list
from org_repo_stats import get_all_forked_repos_in_MLH, get_number_repos_in_MLH


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


def store_all_data():
    pass

print(User("kbanc").user_id)