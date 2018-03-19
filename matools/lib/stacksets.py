import time
from os import path

from core.cloudformation import CloudFormation
from core.ec2 import EC2


class StackSets(object):
    def __init__(self, region):
        self.client = CloudFormation(region=region)
        self.basepath = path.dirname(__file__)

    @staticmethod
    def __get_all_regions():
        ec2_client = EC2(region="ap-southeast-1")

        regions = ec2_client.describe_regions()
        regions = map(lambda x: x["RegionName"], regions)

        regions.remove("ap-southeast-1")
        regions = ["ap-southeast-1"] + regions
        return regions

    @staticmethod
    def __format_tags(tags):
        if len(tags) == 0:
            return []

        formatted_tags = []
        for i in range(len(tags)):
            formatted_tags.append({"Key": tags.keys()[i], "Value": tags.values()[i]})
        return formatted_tags

    @staticmethod
    def __format_parameters(parameters):
        if len(parameters) == 0:
            return []

        formatted_parameters = []
        for i in range(len(parameters)):
            formatted_parameters.append(
                {"ParameterKey": parameters.keys()[i], "ParameterValue": parameters.values()[i]})
        return formatted_parameters

    def __wait_until_created(self, stack_set_name, operation_id, checking_interval=30):
        current_status = "RUNNING"
        while current_status != "SUCCEEDED":
            time.sleep(checking_interval)
            current_status = self.client.describe_stack_set_operation(
                stack_set_name=stack_set_name,
                operation_id=operation_id
            )["Status"]
            if current_status == "FAILED":
                raise RuntimeError("Stack Operation Failed: {}".format(stack_set_name))
            if current_status == "STOPPING" or current_status == "STOPPED":
                break
        return 0

    def create_all_stack_sets(self, stack_sets):
        stack_set_ids = []
        for stack_set in stack_sets:
            tags = {
                "Name": stack_set["name"],
                "Environment": "special",
                "Description": "SPECIAL RESOURCES. DO NOT TOUCH. {}".format(stack_set["description"])
            }

            formatted_tags = self.__format_tags(tags)
            formatted_parameters = self.__format_parameters(stack_set["parameters"])

            rootpath = path.abspath(path.join(self.basepath, ".."))
            filepath = "{}/templates/{}.yml".format(rootpath, stack_set["name"])

            with open(filepath, "r") as opened_file:
                template_body = opened_file.read()

            print("creating stack set: {}".format(stack_set["name"]))
            stack_set_id = self.client.create_stack_set(
                stack_set_name=stack_set["name"],
                description=tags["Description"],
                template_body=template_body,
                tags=formatted_tags,
                parameters=formatted_parameters,
                capabilities=["CAPABILITY_NAMED_IAM"]
            )

            stack_set_ids.append(
                {
                    "StackSetName": stack_set["name"],
                    "StackSetID": stack_set_id
                }
            )
        return stack_set_ids

    def delete_all_stack_sets(self, stack_sets):
        for stack_set in stack_sets:
            self.client.delete_stack_set(stack_set_name=stack_set["name"])
        return 0

    def create_all_stack_instances(self, stack_sets, accounts, parameter_overrides):
        operation_ids = []
        operation_id = ""
        for stack_set in stack_sets:
            regions = self.__get_all_regions() if stack_set["region"] == "all" else [stack_set["region"]]

            for excluded_region in stack_set["excluded_regions"]:
                regions.remove(excluded_region)

            if stack_set["name"] in parameter_overrides:
                for account in parameter_overrides[stack_set["name"]].keys():
                    formatted_parameters = self.__format_parameters(parameter_overrides[stack_set["name"]][account])
                    print("creating stack instances for: {} in {}".format(stack_set["name"], account))
                    operation_id = self.client.create_stack_instances(
                        stack_set_name=stack_set["name"],
                        accounts=[account],
                        regions=regions,
                        parameter_overrides=formatted_parameters,
                        region_order=regions
                    )
                    if stack_set["wait_until_created"]:
                        self.__wait_until_created(stack_set_name=stack_set["name"], operation_id=operation_id)

            else:
                print("creating stack instances for: {}".format(stack_set["name"]))
                operation_id = self.client.create_stack_instances(
                    stack_set_name=stack_set["name"],
                    accounts=accounts,
                    regions=regions,
                    region_order=regions
                )
                if stack_set["wait_until_created"]:
                    self.__wait_until_created(stack_set_name=stack_set["name"], operation_id=operation_id)

            operation_ids.append(
                {
                    "StackSetName": stack_set["name"],
                    "StackSetID": operation_id
                }
            )
        return operation_id

    def delete_all_stack_instances(self, stack_sets, automatic_removal=False):
        operation_ids = []
        for stack_set in stack_sets[::-1]:
            try:
                stack_instances = self.client.list_stack_instances(stack_set_name=stack_set["name"])
            except:  # unable to except specific error (botocore.errorfactory.StackSetNotFoundException)
                continue

            if len(stack_instances) == 0:
                if automatic_removal:
                    self.client.delete_stack_set(stack_set_name=stack_set["name"])
                continue

            accounts = list(set(map(lambda x: x["Account"], stack_instances)))
            regions = list(set(map(lambda x: x["Region"], stack_instances)))

            print("deleting \"{}\"".format(stack_set["name"]))

            operation_id = self.client.delete_stack_instances(
                stack_set_name=stack_set["name"],
                accounts=accounts,
                regions=regions,
                region_order=regions
            )

            operation_ids.append(
                {
                    "StackSetName": stack_set["name"],
                    "OperationID": operation_id
                }
            )
        return operation_ids

    def complete_removal(self, stack_sets):
        operation_ids = self.delete_all_stack_instances(stack_sets=stack_sets, automatic_removal=True)
        while len(operation_ids) > 0:
            for operation_id in operation_ids:
                status = self.client.describe_stack_set_operation(
                    stack_set_name=operation_id["StackSetName"],
                    operation_id=operation_id["OperationID"]
                )["Status"]
                if status == "SUCCEEDED":
                    self.client.delete_stack_set(stack_set_name=operation_id["StackSetName"])
                    operation_ids.remove(operation_id)
                elif status == "FAILED":
                    raise RuntimeError("Stack Operation Failed: {}".format(operation_id["StackSetName"]))
            time.sleep(30)
        return 0

    def retry_failed_operation(self, stack_set):
        tags = {
            "Name": stack_set["name"],
            "Environment": "special",
            "Description": "SPECIAL RESOURCES. DO NOT TOUCH. {}".format(stack_set["description"])
        }

        formatted_tags = self.__format_tags(tags)
        formatted_parameters = self.__format_parameters(stack_set["parameters"])

        regions = self.__get_all_regions() if stack_set["region"] == "all" else [stack_set["region"]]

        for excluded_region in stack_set["excluded_regions"]:
            regions.remove(excluded_region)

        self.client.update_stack_set(
            stack_set_name=stack_set["name"],
            description=stack_set["description"],
            tags=formatted_tags,
            parameters=formatted_parameters,
            capabilities=["CAPABILITY_NAMED_IAM"],
            region_order=regions
        )
        return 0
