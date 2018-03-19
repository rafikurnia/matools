import boto3


class EC2(object):
    def __init__(self, region):
        self.client = boto3.client("ec2", region)

    def describe_regions(self):
        regions = self.client.describe_regions()["Regions"]
        return regions
