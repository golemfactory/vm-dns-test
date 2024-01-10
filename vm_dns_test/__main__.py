import asyncio
from typing import Awaitable

from yapapi.log import enable_default_logger

from . import tasks, utils

DEFAULT_NUM_HOSTS = 5


if __name__ == "__main__":
    parser = utils.argument_parser()
    parser.add_argument("-w", "--num-workers", type=int, help="Number of provider hosts to run the tests on. default=%(default)s", default=5)
    parser.add_argument("-b", "--num-batches", type=int, help="Number of provider hosts to run the tests on. default=%(default)s", default=5)
    parser.add_argument("-r", "--num-requests", type=int, help="Number of requests per host. default=%(default)s", default=10)
    args = parser.parse_args()

    enable_default_logger(
        log_file=args.log_file,
        debug_activity_api=True,
        debug_market_api=True,
        debug_payment_api=True,
        debug_net_api=True,
    )

    async def run_tasks(run: Awaitable):
        task = asyncio.create_task(run)

        try:
            await task
        except KeyboardInterrupt:
            print("Shutting down...")
            task.cancel()
            try:
                await task
                print("Shutdown completed.")
            except (asyncio.CancelledError, KeyboardInterrupt):
                pass

    asyncio.run(
        run_tasks(
            tasks.run(
                num_workers=args.num_workers,
                num_batches=args.num_batches,
                num_requests=args.num_requests,
                subnet_tag=args.subnet_tag,
                payment_driver=args.payment_driver,
                payment_network=args.payment_network,
            )
        )
    )
