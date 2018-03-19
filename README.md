# matools
Tools to automate scaffolding resources setup processes.

## Installation
```bash
pip install git+ssh://git@github.com:rafikurnia/matools.git
```

## Config File
In order to use this tools, you need to create config file.
The example file is on example/example-config.yml

## Quickstart
```bash
# Show help
matools -h

# Check your yml file
awsudo -u sa@acc-org -- matools test --configfile example/example-config.yml 

# Create all Stack Sets and All Stack Set Instances
awsudo -u sa@acc-org -- matools create-all --configfile example/example-config.yml 

# Create all Stack Set Instances only
awsudo -u sa@acc-org -- matools create-stack-instances --configfile example/example-config.yml 

# Delete all Stack Set Instances and Stack Sets (Dangerous Command) 
awsudo -u sa@acc-org -- matools delete-all --configfile example/example-config.yml 
```


## Authors
[Rafi Kurnia Putra](https://github.com/rafikurnia)