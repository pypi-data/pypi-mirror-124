# -*- coding: utf-8 -*-

import argparse

from tuxsuite.cli.version import __version__

from tuxsuite.cli.build import setup_parser as build_parser
from tuxsuite.cli.group import setup_parser as group_parser
from tuxsuite.cli.plan import setup_parser as plan_parser
from tuxsuite.cli.project import setup_parser as project_parser
from tuxsuite.cli.test import setup_parser as test_parser


def setup_parser(group, project):
    parser = argparse.ArgumentParser(prog="tuxsuite", description="tuxsuite")

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s, {__version__}"
    )

    parser.add_argument("--group", default=group)
    parser.add_argument("--project", default=project)

    root = parser.add_subparsers(dest="sub_command", help="Sub commands")
    root.required = True

    # "build"
    build = root.add_parser("build", help="builds").add_subparsers(
        dest="sub_sub_command", help="Sub commands"
    )
    build.required = True
    build_parser(build)

    # "group"
    group = root.add_parser("group", help="groups").add_subparsers(
        dest="sub_sub_command", help="Sub commands"
    )
    group.required = True
    group_parser(group)

    # "plan"
    plan = root.add_parser("plan", help="plans").add_subparsers(
        dest="sub_sub_command", help="Sub commands"
    )
    plan.required = True
    plan_parser(plan)

    # "project"
    project = root.add_parser("project", help="projects").add_subparsers(
        dest="sub_sub_command", help="Sub commands"
    )
    project.required = True
    project_parser(project)

    # "test"
    test = root.add_parser("test", help="tests").add_subparsers(
        dest="sub_sub_command", help="Sub commands"
    )
    test.required = True
    test_parser(test)

    return parser
