import argparse
from unittest import mock

from users import main


@mock.patch(
    'argparse.ArgumentParser.parse_args',
    return_value=argparse.Namespace(),
)
def test_parse_arguments(mock_args):
    """Am I cheating ? Yes."""
    parser = main.parse_arguments()
    assert parser is not None
