import os
import shutil

from management import config


def test_config_init_01():
    """This check should enter in the first if statement."""
    assert config.config_init() == 0


def test_config_init_02():
    """Create config file and check that it exists."""
    folder_path = f"{os.getenv('HOME')}/.mybookingservices"
    config_file = f"{folder_path}/management_api.conf"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    config.config_init()
    assert os.path.exists(config_file) is True


def test_check_config_03():
    """This check should enter in the first if statement."""
    assert config.config_init() == 0


def test_check_config_01():
    """Check for check_config."""
    folder_path = f"{os.getenv('HOME')}/.mybookingservices"
    shutil.rmtree(folder_path)
    assert config.check_config() is None


def test_check_config_02():
    """Check for check_config."""
    folder_path = f"{os.getenv('HOME')}/.mybookingservices"
    config_file = f"{folder_path}/management_api.conf"
    config.config_init()
    assert config.check_config() == config_file


def test_config_api_setup_01():
    folder_path = f"{os.getenv('HOME')}/.mybookingservices"
    shutil.rmtree(folder_path)
    assert config.config_api_setup() is None
    config.config_init()
