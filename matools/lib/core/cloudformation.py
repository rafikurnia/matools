import boto3


class CloudFormation(object):
    def __init__(self, region):
        self.client = boto3.client("cloudformation", region)

    def create_stack_set(self, stack_set_name, description, tags, template_body, parameters=None, capabilities=None):
        if parameters is None:
            parameters = []
        if capabilities is None:
            capabilities = []

        stack_set_id = self.client.create_stack_set(
            StackSetName=stack_set_name,
            Description=description,
            TemplateBody=template_body,
            Parameters=parameters,
            Capabilities=capabilities,
            Tags=tags
        )["StackSetId"]

        return stack_set_id

    def delete_stack_set(self, stack_set_name):
        response = self.client.delete_stack_set(
            StackSetName=stack_set_name
        )
        return response

    def describe_stack_set(self, stack_set_name):
        stack_set_info = self.client.describe_stack_set(
            StackSetName=stack_set_name
        )["StackSet"]
        return stack_set_info

    def list_stack_sets(self, status):
        summaries = self.client.list_stack_sets(
            Status=status
        )["Summaries"]
        return summaries

    def update_stack_set(self, stack_set_name, description, tags, parameters=None, capabilities=None, region_order=None):
        if parameters is None:
            parameters = []
        if capabilities is None:
            capabilities = []
        if region_order is None:
            region_order = []

        operation_id = self.client.update_stack_set(
            StackSetName=stack_set_name,
            Description=description,
            UsePreviousTemplate=True,
            Parameters=parameters,
            Capabilities=capabilities,
            Tags=tags,
            OperationPreferences={
                "RegionOrder": region_order,
                "FailureTolerancePercentage": 0,
                "MaxConcurrentPercentage": 100
            }
        )["OperationId"]
        return operation_id

    def create_stack_instances(self, stack_set_name, accounts, regions, parameter_overrides=None, region_order=None):
        if parameter_overrides is None:
            parameter_overrides = []
        if region_order is None:
            region_order = []

        operation_id = self.client.create_stack_instances(
            StackSetName=stack_set_name,
            Accounts=accounts,
            Regions=regions,
            ParameterOverrides=parameter_overrides,
            OperationPreferences={
                "RegionOrder": region_order,
                "FailureTolerancePercentage": 0,
                "MaxConcurrentPercentage": 100
            }
        )["OperationId"]
        return operation_id

    def delete_stack_instances(self, stack_set_name, accounts, regions, region_order=None):
        if region_order is None:
            region_order = []

        operation_id = self.client.delete_stack_instances(
            StackSetName=stack_set_name,
            Accounts=accounts,
            Regions=regions,
            OperationPreferences={
                "RegionOrder": region_order,
                "FailureTolerancePercentage": 0,
                "MaxConcurrentPercentage": 100
            },
            RetainStacks=False
        )["OperationId"]
        return operation_id

    def describe_stack_instance(self, stack_set_name, stack_instance_account, stack_instance_region):
        stack_instance_info = self.client.describe_stack_instance(
            StackSetName=stack_set_name,
            StackInstanceAccount=stack_instance_account,
            StackInstanceRegion=stack_instance_region
        )["StackInstance"]
        return stack_instance_info

    def list_stack_instances(self, stack_set_name):
        summaries = self.client.list_stack_instances(
            StackSetName=stack_set_name,
        )["Summaries"]
        return summaries

    def update_stack_instances(self, stack_set_name, accounts, regions, parameter_overrides=None, region_order=None):
        if region_order is None:
            region_order = []
        if parameter_overrides is None:
            parameter_overrides = []

        operation_id = self.client.update_stack_instances(
            StackSetName=stack_set_name,
            Accounts=accounts,
            Regions=regions,
            ParameterOverrides=parameter_overrides,
            OperationPreferences={
                "RegionOrder": region_order,
                "FailureTolerancePercentage": 0,
                "MaxConcurrentPercentage": 100
            }
        )["OperationId"]
        return operation_id

    def describe_stack_set_operation(self, stack_set_name, operation_id):
        stack_set_operation = self.client.describe_stack_set_operation(
            StackSetName=stack_set_name,
            OperationId=operation_id
        )["StackSetOperation"]
        return stack_set_operation
