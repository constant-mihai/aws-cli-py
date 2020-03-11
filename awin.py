#!/usr/bin/python3
from termcolor import colored
import pprint
import boto3
import fillin

DEFAULT_REGION = "eu-west-1"
DEFAULT_FILTERS =  [{
    # 'Name': 'tag:Name',
    # 'Values': ['*']
    }]

def filter_instances(base, filters=None):
    """
    Filters the ec2 instances.
    """

    if filters == None:
        filters = DEFAULT_FILTERS

    filtered = base.filter(Filters=filters)

    ret = []
    for i in filtered:
        el = {}
        name = ""
        if i.tags != None:
            for t in i.tags:
                if t['Key'] == 'Name':
                    name = t['Value']
        el["name"] = name
        el["id"] = i.id
        el["public_ip_address"] = i.public_ip_address
        el["private_ip_address"] = i.private_ip_address
        el["state"] = i.state
        ret.append(el)
    return ret

def get_state_color(detail):
    d = detail
    state = d["state"]["Name"]
    state_color = "yellow"
    if state == "running":
        state_color = "green"
    elif state == "stopped":
        state_color = "red"
    elif state == "terminated":
        state_color = "red"

    return colored(d["state"]["Name"], state_color, attrs=["bold"])

def print_instance_details(details):
    name = dict()
    public_ip = dict()
    private_ip = dict()
    instance = dict()
    state = dict()
    for d in details:
        state_color = "white"
        name["key"] = colored("Name", 'yellow')
        name["val"] = d["name"]
        instance["key"] = colored("Instance id", 'yellow')
        instance["val"] = d["id"]
        public_ip["key"] = colored("Public Ip", 'yellow')
        public_ip["val"] = d["public_ip_address"]
        private_ip["key"] = colored("Private Ip", 'yellow')
        private_ip["val"] = d["private_ip_address"]
        state["key" ] = colored("State", 'yellow')
        state["val" ] = get_state_color(d)

        print("{}: {:>35} {}: {} {}: {:>15} {}: {:>15} {}: {}"
                .format(name["key"], name["val"],
                    instance["key"], instance["val"],
                    public_ip["key"], str(public_ip["val"]),
                    private_ip["key"], str(private_ip["val"]),
                    state["key"], state["val"]))

"""
Main
"""
region = input("Region [default: eu-west-1]: ")
if region == "":
    region = DEFAULT_REGION

ec2 = boto3.resource('ec2', region)

base = ec2.instances.filter()

# instance_filters = []
# instance_filters.append({'Name': 'tag:Squad', 'Values': ['*']})
# tags = fillin.ask_for_tags()
details = filter_instances(base)
print_instance_details(details)
