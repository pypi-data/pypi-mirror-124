# -*- coding: utf-8 -*-

import configparser
from dataclasses import dataclass
import os
from pathlib import Path


@dataclass
class Config:
    group: str
    project: str
    token: str
    tuxapi_url: str


def load_config():
    defaults = Path.home() / ".config" / "tuxsuite" / "defaults.ini"
    path = Path.home() / ".config" / "tuxsuite" / "config.ini"
    env = os.environ.get("TUXSUITE_ENV", "default")

    try:
        config = configparser.ConfigParser()
        config.read([defaults, path])
    except configparser.Error as exc:
        raise NotImplementedError(exc)
    if not config.has_section(env):
        raise NotImplementedError(f"Missing section {env}")

    return Config(
        group=config[env].get("group"),
        project=config[env].get("project"),
        token=config[env].get("token"),
        tuxapi_url=config[env].get("tuxapi_url", "https://tuxapi.tuxsuite.com"),
    )
