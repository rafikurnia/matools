from core.cloudwatch_logs import LogGroup
from core.ec2 import EC2


class Logs(object):
    def __init__(self, region):
        self.ec2_client = EC2(region=region)

    def delete_log_group_from_all_regions(self, log_group_name):
        regions = self.ec2_client.describe_regions()
        regions = map(lambda x: x["RegionName"], regions)
        for region in regions:
            print(region)
            log_group = LogGroup(region=region)

            if len(log_group.describe_log_groups(log_group_name_prefix=log_group_name)) > 0:
                log_group.delete_log_group(log_group_name=log_group_name)
                print("Deleted")
            else:
                print("Not found")
