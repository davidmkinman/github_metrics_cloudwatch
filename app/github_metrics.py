import os
import typing

from datetime import datetime
from github import Github

from cloudwatch_metric import StatisticMetric, ValueMetric


class GithubOrgMetrics:

    def __init__(
            self,
            github_url: str = "",
            github_org: str = "mobile",
            github_token: str = "",
            library_banlist: typing.List[str] = list(),
    ):

        self.library_banlist = library_banlist
        github_url = (
            os.environ.get("GITHUB_URL") if github_url == "" else github_url
        )
        github_token = (
            os.environ.get("GITHUB_TOKEN") if github_token == "" else github_token
        )
        # self.github = github.Github(
        #     base_url=github_url,
        #     login_or_token=github_token,
        # )
        self.github = Github(
            github_token
        )
        self.org = self.github.get_organization(github_org)

    def report_open_pull_requests(self, repo):
        """
        Push the
        :return:
        """
        metric = datetime.now().second
        pulls: typing.PaginatedList = repo.get_pulls()
        pull_list = list(pulls)
        print(pull_list[0])
        self.__send_metric(
            metric_name="OpenPullRequests",
            repository_name=repo.name,
            value=pulls.totalCount
        )

    def open_pulls_gauge(self, pulls, repo):
        metric = ValueMetric(
            metric_name="OpenPullRequests",
            repository_name=repo.name,
            value=len(pulls)
        )
        return metric

    def __time_units(self, time_period):
        """
        length of time period in hours
        """
        return int(time_period.days * 24 + time_period.seconds / 3600)

    def pulls_age_stats(self, pulls: typing.List, repo):
        now = datetime.now()
        pull_age: typing.List[int] = [
            self.__time_units(now - pull.created_at)
            for pull in pulls
        ]
        metric = StatisticMetric(
            metric_name="OpenPullsAge",
            repository_name=repo.name,
            values=pull_age
        )
        return metric

    def pulls_last_update_age_stats(self, pulls: typing.List, repo):
        now = datetime.now()
        pull_age: typing.List[int] = [
            self.__time_units(now - pull.updated_at)
            for pull in pulls
        ]
        metric = StatisticMetric(
            metric_name="OpenPullsLastUpdateAge",
            repository_name=repo.name,
            values=pull_age,
        )
        return metric

    def collect_pulls_metrics(self, repo):
        metrics: typing.List[ValueMetric] = []

        pulls: typing.List[Github.PullRequest] = list(repo.get_pulls())
        metrics.append(self.open_pulls_gauge(pulls, repo))
        metrics.append(self.pulls_age_stats(pulls, repo))
        metrics.append(self.pulls_last_update_age_stats(pulls, repo))

        # publish metrics
        for metric in metrics:
            response = metric.publish_metric()
            print(response)

    def collect_metrics(self):
        #for repo in self.org.get_repos():
        for repo in [self.org.get_repo('k8s-conformance')]:
            self.collect_pulls_metrics(repo=repo)
