#!/usr/bin/env python3
"""config module related to the config file."""
import configparser
import os
from pathlib import Path
from typing import Optional
from typing import Tuple
from typing import Union


def get_config() -> Tuple[str, str]:
    """Get config path and config file path.
    This function returns the path of the dir
    containing the config file, and the config file itself.
    """
    home_dir = os.getenv('HOME')
    config_path = f"{home_dir}/.mybookingservices"
    config_file = f"{config_path}/booking_api.conf"

    return config_path, config_file


def config_init() -> int:
    """Init config file if needed."""
    config_path, config_file = get_config()

    if Path(config_file).exists():
        print("[i] config file already exists")
        return 0

    if not os.path.exists(config_path):
        os.makedirs(config_path)

    config = configparser.ConfigParser()
    config['database'] = {}
    config['database']['connector'] = 'mysql+pymysql'
    config['database']['user'] = 'etna'
    config['database']['password'] = 'etna'
    config['database']['host'] = 'localhost'
    config['database']['database'] = 'mybookingservices'

    with open(config_file, 'w') as configfile:
        config.write(configfile)

    print(f"[i] config file created at {config_file}.")
    return 0


def check_config() -> Optional[str]:
    """Check if config file exists. Returns either str or None."""
    config_file = get_config()[1]
    if not Path(config_file).exists():
        print(f"[w] config file not found : {config_file}")
        return None
    return config_file


def config_api_setup() -> Union[
    None,
    Tuple[configparser.ConfigParser, str],
]:
    """Open and read config file.
    This function returns the content of the
    config file as a ConfigParser object and the str to the file.
    """
    config_file = check_config()
    if config_file is None:
        print("[e] could not setup api config file")
        return None
    config = configparser.ConfigParser()
    return config, config_file
