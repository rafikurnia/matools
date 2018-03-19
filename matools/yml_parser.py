import datetime

import yaml


def parse_yml(file_path):
    yml_contents = {}
    with open(file_path, "r") as stream:
        try:
            yml_contents = yaml.load(stream)
        except yaml.YAMLError as e:
            raise yaml.YAMLError("Something wrong with your configuration file: {}".format(e))

    try:
        version = yml_contents["MatoolsTemplateVersion"]
    except KeyError:
        raise ValueError("You should provide 'MatoolsTemplateVersion'")

    version = version.strftime("%Y-%m-%d") if isinstance(version, datetime.date) else version
    if version != "2018-03-15":
        raise AttributeError("Currently supported version is only: 2018-03-15")

    try:
        accounts = map(lambda x: str(x), yml_contents["Accounts"])
    except KeyError:
        raise ValueError("You should provide 'Accounts'")

    if len(accounts) == 0:
        raise ValueError("You should provide at least one AWS Account ID")

    try:
        enabled_stack_sets = yml_contents["StackSets"]
    except KeyError:
        raise ValueError("You should provide 'StackSets'")

    if "default-superadmin-role" in enabled_stack_sets:
        try:
            admins = ",".join(yml_contents["AccountAdministrators"])
        except KeyError:
            raise ValueError("You should provide 'AccountAdministrators'")
    else:
        admins = ""

    if "default-cloudconformity-monitoring" in enabled_stack_sets:
        try:
            parameter_overrides = yml_contents["ParameterOverrides"]
        except KeyError:
            raise ValueError("You should provide 'ParameterOverrides'")

        try:
            cloudconformity_monitoring = parameter_overrides["default-cloudconformity-monitoring"]
        except KeyError:
            raise ValueError("You should provide 'ParameterOverrides.default-cloudconformity-monitoring'")

        try:
            auth_tokens = cloudconformity_monitoring["CloudConformityAuthenticationToken"]
        except KeyError:
            raise ValueError(
                "You should provide "
                "'ParameterOverrides.default-cloudconformity-monitoring.CloudConformityAuthenticationToken'"
            )

        if len(auth_tokens) != len(yml_contents["Accounts"]):
            raise ValueError("Parameter count mismatch with number of accounts")

        cloudconformity_rtm_tokens = {}
        for i in range(len(auth_tokens)):
            cloudconformity_rtm_tokens[accounts[i]] = {"CloudConformityAuthenticationToken": auth_tokens[i]}
    else:
        cloudconformity_rtm_tokens = {}

    return accounts, enabled_stack_sets, admins, cloudconformity_rtm_tokens
