import asyncio

from yapapi.log import enable_default_logger


from . import tasks, utils


if __name__ == "__main__":
    parser = utils.argument_parser()
    args = parser.parse_args()

    enable_default_logger(
        log_file=args.log_file,
        debug_activity_api=True,
        debug_market_api=True,
        debug_payment_api=True,
        debug_net_api=True,
    )

    asyncio.run(
        tasks.run_tasks(
            subnet_tag=args.subnet_tag,
            payment_driver=args.payment_driver,
            payment_network=args.payment_network,
        )
    )
