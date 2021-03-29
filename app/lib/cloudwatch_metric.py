import typing
import boto3

from datetime import datetime



class CloudwatchMetric:
    cloudwatch = boto3.client('cloudwatch')

    def __init__(
            self,
            metric_name: str,
            repository_name: str,
            unit: str = 'None'
    ):
        self.metric_name = metric_name
        self.repository_name = repository_name
        self.unit = unit

        self.namespace = "HSBC/Github"

    def publish_metric(self):
        pass

    def _metric_timestamp(self) -> str:
        """
        create a timestamp string in format for AWS cloudwatch metrics
        :return: cloudwatch metric timestamp
        """
        return datetime.now().strftime("%b %d %Y %H:%M:%S %Z")

    def _post_metric(self, metric_datum: typing.List):
        response = self.cloudwatch.put_metric_data(
            MetricData=metric_datum,
            Namespace=self.namespace
        )
        print(response)
        return response


class ValueMetric(CloudwatchMetric):
    def __init__(
            self,
            metric_name: str,
            repository_name: str,
            value: any,
            unit: str = 'None'
    ):
        super().__init__(
            metric_name,
            repository_name,
            unit
        )
        self.value = value

    def publish_metric(self):
        """
        Send a metric to the monitoring solution (currently cloudwatch)
        :return: response
        """
        metric_datum = [
            {
                'MetricName': self.metric_name,
                'Dimensions': [
                    {
                        'Name': 'Name',
                        'Value': self.repository_name,
                    },
                ],
                'Timestamp': self._metric_timestamp(),
                'Unit': self.unit,
                'Value': self.value
            },
        ]
        print(metric_datum)

        response = self._post_metric(metric_datum)
        return response


class StatisticMetric(CloudwatchMetric):
    def __init__(
            self,
            metric_name: str,
            repository_name: str,
            values: typing.List[int],
            unit: str = 'None'
    ):
        super().__init__(
            metric_name,
            repository_name,
            unit
        )
        self.sample_count = len(values)
        self.sum = sum(values) if self.sample_count > 0 else 0
        self.min = min(values) if self.sample_count > 0 else 0
        self.max = max(values) if self.sample_count > 0 else 0

    def publish_metric(self):
        """
        Send a metric to the monitoring solution (currently cloudwatch)
        :return:
        """
        if self.sample_count == 0:
            # We cannot publish empty data, no pulls === no data to record
            return
        metric_datum = [
            {
                'MetricName': self.metric_name,
                'Dimensions': [
                    {
                        'Name': 'Name',
                        'Value': self.repository_name,
                    },
                ],
                'Timestamp': self._metric_timestamp(),
                'Unit': self.unit,
                'StatisticValues': {
                    'Sum': self.sum,
                    'Minimum': self.min,
                    'Maximum': self.max,
                    'SampleCount': self.sample_count
                }
            },
        ]
        print(metric_datum)

        response = self._post_metric(metric_datum)
        return response
