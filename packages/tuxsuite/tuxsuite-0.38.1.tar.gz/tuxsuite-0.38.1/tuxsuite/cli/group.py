# -*- coding: utf-8 -*-

from tuxsuite.cli.requests import get

import json


def format_int(v):
    if v > 1e6:
        return f"{int(v // 1e6)}M"
    if v > 1e3:
        return f"{int(v // 1e3)}k"
    return str(v)


def handle_bills(options, config):
    ret = get(config, f"/v1/groups/{options.name}/bills")
    if ret.status_code != 200:
        raise NotImplementedError()

    if options.json:
        print(json.dumps(ret.json()))
    else:
        print("date\t\tbuilds\tplans\ttests\tbuilds\ttests")
        for bill in ret.json()["results"]:
            builds = bill["count"]["builds"]
            plans = bill["count"]["plans"]
            tests = bill["count"]["tests"]
            d_builds = format_int(bill["duration"]["builds"])
            d_tests = format_int(bill["duration"]["tests"])
            print(f"{bill['date']}\t{builds}\t{plans}\t{tests}\t{d_builds}\t{d_tests}")
    return 0


def handle_get(options, config):
    ret = get(config, f"/v1/groups/{options.name}")
    if ret.status_code != 200:
        raise NotImplementedError()

    if options.json:
        print(json.dumps(ret.json()))
    else:

        def tripplet(d):
            return f"{d['daily']} / {d['monthly']} / {d['overall']}"

        grp = ret.json()
        print(f"name    : {grp['name']}")
        print(f"builds  : {tripplet(grp['builds'])}")
        print(f"plans   : {tripplet(grp['plans'])}")
        print(f"tests   : {tripplet(grp['tests'])}")
        print(
            f"duration: builds={grp['duration']['builds']} tests={grp['duration']['tests']}"
        )
    return 0


def handle_list(options, config):
    ret = get(config, "/v1/groups")
    if ret.status_code != 200:
        raise NotImplementedError()

    if options.json:
        print(json.dumps(ret.json()))
    else:
        print("groups:")
        for grp in ret.json()["results"]:
            print(f"* {grp}")
    return 0


handlers = {
    "bills": handle_bills,
    "get": handle_get,
    "list": handle_list,
}


def setup_parser(parser):
    # "group bills <name>"
    p = parser.add_parser("bills")
    p.add_argument("name")
    p.add_argument("--json", action="store_true")

    # "group get <name>"
    p = parser.add_parser("get")
    p.add_argument("name")
    p.add_argument("--json", action="store_true")

    # "group list"
    p = parser.add_parser("list")
    p.add_argument("--json", action="store_true")
