from pprint import pprint

from lib.stacksets import StackSets
from yml_parser import parse_yml


def __initialize(file_path):
    accounts, enabled_stack_sets, admins, cloudconformity_rtm_tokens = parse_yml(file_path)

    stack_sets = []
    if "default-s3-buckets" in enabled_stack_sets:
        stack_sets.append(
            {
                "name": "default-s3-buckets",
                "region": "ap-southeast-1",
                "excluded_regions": [],
                "description": "This StackSet will create several S3 Buckets that are used for scaffolding resources.",
                "parameters": {},
                "wait_until_created": True
            }
        )
    if "default-service-roles" in enabled_stack_sets:
        stack_sets.append(
            {
                "name": "default-service-roles",
                "region": "us-east-1",
                "excluded_regions": [],
                "description": "This StackSet will create several IAM Roles for scaffolding resources.",
                "parameters": {},
                "wait_until_created": True
            }
        )
    if "default-guardduty" in enabled_stack_sets:
        stack_sets.append(
            {
                "name": "default-guardduty",
                "region": "all",
                "excluded_regions": ["eu-west-3"],
                "description": "this StackSet will enable Amazon GuardDuty.",
                "parameters": {},
                "wait_until_created": False
            }
        )
    if "default-config" in enabled_stack_sets:
        stack_sets.append(
            {
                "name": "default-config",
                "region": "all",
                "excluded_regions": [],
                "description": "This StackSet will enable AWS Config.",
                "parameters": {},
                "wait_until_created": False
            }
        )
    if "default-cloudtrail" in enabled_stack_sets:
        stack_sets.append(
            {
                "name": "default-cloudtrail",
                "region": "ap-southeast-1",
                "excluded_regions": [],
                "description": "This StackSet will enable AWS CloudTrail.",
                "parameters": {},
                "wait_until_created": False
            }
        )
    if "default-superadmin-role" in enabled_stack_sets:
        stack_sets.append(
            {
                "name": "default-superadmin-role",
                "region": "us-east-1",
                "excluded_regions": [],
                "description": "This StackSet will create a temporary IAM Role for account administrator.",
                "parameters": {
                    "AdministratorRoleARNs": admins
                },
                "wait_until_created": False
            }
        )
    if "default-terraform-state-management" in enabled_stack_sets:
        stack_sets.append(
            {
                "name": "default-terraform-state-management",
                "region": "ap-southeast-1",
                "excluded_regions": [],
                "description": "This StackSet will create S3 Bucket and DynamoDB Table for Terraform State management.",
                "parameters": {},
                "wait_until_created": False
            }
        )
    if "default-cloudconformity-monitoring" in enabled_stack_sets:
        stack_sets.append(
            {
                "name": "default-cloudconformity-monitoring",
                "excluded_regions": [],
                "region": "all",
                "description": "This StackSet will enable CloudConformity Real-Time Threat Monitoring.",
                "parameters": {
                    "CloudConformityAuthenticationToken": ""
                },
                "wait_until_created": True
            }
        )

    parameter_overrides = {
        "default-cloudconformity-monitoring": cloudconformity_rtm_tokens
    }

    cfn_client = StackSets(region="ap-southeast-1")

    return accounts, stack_sets, parameter_overrides, cfn_client, enabled_stack_sets


def create_all(args):
    accounts, stack_sets, parameter_overrides, cfn_client, _ = __initialize(args.configfile)

    stack_ids = cfn_client.create_all_stack_sets(stack_sets=stack_sets)
    print(stack_ids)

    operation_ids = cfn_client.create_all_stack_instances(
        stack_sets=stack_sets,
        accounts=accounts,
        parameter_overrides=parameter_overrides
    )
    print(operation_ids)


def create_stack_sets(args):
    _, stack_sets, _, cfn_client, _ = __initialize(args.configfile)

    stack_ids = cfn_client.create_all_stack_sets(stack_sets=stack_sets)
    print(stack_ids)


def create_stack_instances(args):
    accounts, stack_sets, parameter_overrides, cfn_client, _ = __initialize(args.configfile)

    operation_ids = cfn_client.create_all_stack_instances(
        stack_sets=stack_sets,
        accounts=accounts,
        parameter_overrides=parameter_overrides
    )
    print(operation_ids)


def delete_all(args):
    _, stack_sets, _, cfn_client, _ = __initialize(args.configfile)

    cfn_client.complete_removal(stack_sets=stack_sets)


def test(args):
    accounts, stack_sets, parameter_overrides, cfn_client, enabled_stack_sets = __initialize(args.configfile)

    print("Accounts:")
    pprint(accounts, indent=4)
    print("")

    print("StackSets:")
    pprint(enabled_stack_sets, indent=4)
    print("")

    print("ParameterOverrides:")
    pprint(parameter_overrides, indent=4)
    print("")
