#!/usr/bin/python3
from termcolor import colored
import boto3
import os
#import fillin
import argparse
import sys

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

def parse_args(argv):
    """ Parse arguments """
    parser = argparse.ArgumentParser(description = 'AWS cli')
    parser.add_argument('--instance-id',
            dest = 'instance_id',
            help = 'Instance Id',
            type = str)
    return parser.parse_args(argv[1:])

def main(argv):
    """
    Main
    """
    args = parse_args(argv)
    region = os.getenv('AWS_REGION', "eu-west-1")
    ec2 = boto3.resource('ec2', region)
    # tags = fillin.ask_for_tags()
    #instance_filters = []
    #instance_filters.append({'Name': 'instance-id', 'Values': [args.instance_id]})

    if args.instance_id:
        base = ec2.instances.filter(InstanceIds=[args.instance_id])
        # print(dir(base))
        # print(vars(base))
        for i in base:
            # print(dir(i))
            # print(vars(i))
            print("Tags:")
            for t in i.tags:
                print("\t{:<30}: {}".format(t['Key'], t['Value']))
    else:
        base = ec2.instances.filter()
        details = filter_instances(base)
        print_instance_details(details)


if __name__ == '__main__':
    main(sys.argv)
