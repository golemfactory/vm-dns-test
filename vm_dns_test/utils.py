import argparse
from datetime import datetime, timezone

from yapapi import Golem
from yapapi import __version__ as yapapi_version


def print_env_info(golem: Golem):
    print(
        f"yapapi version: {yapapi_version}, "
        f"subnet: {golem.subnet_tag}, "
        f"payment platform: {golem.payment_driver}/{golem.payment_network}\n"
    )


def argument_parser():
    current_time_str = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S%z")
    default_log_path = f"vm-dns-test-{current_time_str}.log"

    parser = argparse.ArgumentParser("vm dns tester")
    parser.add_argument(
        "--payment-driver", "--driver", help="Payment driver name, for example `erc20`"
    )
    parser.add_argument(
        "--payment-network", "--network", help="Payment network name, for example `goerli`"
    )
    parser.add_argument("--subnet-tag", help="Subnet name, for example `public`")
    parser.add_argument(
        "--log-file",
        default=str(default_log_path),
        help="Log file for YAPAPI; default: %(default)s",
    )
    return parser
