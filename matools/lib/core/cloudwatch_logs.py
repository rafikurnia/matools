import boto3


class LogGroup(object):

    def __init__(self, region):
        self.client = boto3.client('logs', region)

    def describe_log_groups(self, log_group_name_prefix):
        log_groups = self.client.describe_log_groups(
            logGroupNamePrefix=log_group_name_prefix,
        )["logGroups"]

        return log_groups

    def delete_log_group(self, log_group_name):
        self.client.delete_log_group(
            logGroupName=log_group_name,
        )
