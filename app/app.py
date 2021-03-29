import json

from lib.github_metrics import GithubOrgMetrics

def lambda_handler(event, context):
    metrics = GithubOrgMetrics(
        github_org="cncf",
        github_url="https://api.github.com"
    )
    metrics.collect_metrics()
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
        }),
    }


if __name__ == '__main__':
    metrics = GithubOrgMetrics(
        github_org="cncf",
        github_url="https://api.github.com/"
    )
    metrics.collect_metrics()
