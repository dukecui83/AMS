#!/usr/bin/env python
# coding: utf-8

import json

from setproctitle import setproctitle

from ams.helpers import Topic
from ams.nodes import User

from argument_parser import parser
from clients.helper import get_manager_client, get_redis_client, get_paho_client, get_aws_iot_client


if __name__ == '__main__':

    setproctitle("ams_user")

    parser.add_argument(
        "-SMP", "--state_machine_path", type=str, default=None, help="state machine resource path")
    args = parser.parse_args()

    if args.kvs_client_type == "manager":
        kvs_client = get_manager_client()
    elif args.kvs_client_type == "redis":
        kvs_client = get_redis_client(args.kvs_host)
    else:
        raise ValueError("Unknown kvs client type: {}".format(args.kvs_client_type))

    if args.pubsub_client_type == "paho":
        pubsub_client = get_paho_client(args.pubsub_host, args.pubsub_port)
    elif args.pubsub_client_type == "aws_iot":
        pubsub_client = get_aws_iot_client(
            args.pubsub_host, args.pubsub_port, args.path_ca, args.path_private_key, args.path_cert)
    else:
        raise ValueError("Unknown pubsub client type: {}".format(args.pubsub_client_type))

    with open(args.initials_file_path, "r") as f:
        initials = json.load(f)

    Topic.domain = args.topic_domain

    user = User(initials["config"], initials["status"], args.state_machine_path)
    user.set_rate(args.event_loop_rate)
    user.set_clients(kvs_client, pubsub_client)
    user.start()