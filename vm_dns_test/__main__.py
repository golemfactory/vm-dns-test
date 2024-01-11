import asyncio
import colorful
from typing import Awaitable

from yapapi.log import enable_default_logger

from . import tasks, utils

DEFAULT_NUM_HOSTS = 5


if __name__ == "__main__":
    parser = utils.argument_parser()
    parser.add_argument("-w", "--num-workers", type=int, help="Number of concurrent workers. default=%(default)s", default=10)
    parser.add_argument("-b", "--num-batches", type=int, help="Overall number of batches/tasks to run. default=%(default)s", default=1000)
    parser.add_argument("-r", "--num-requests", type=int, help="Number of requests per batch. default=%(default)s", default=10)
    parser.add_argument("-t", "--num-batches-per-worker", type=int, help="Number of batches (tasks) per a single worker run. default=%(default)s", default=100)
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

    print(f"Run arguments: {colorful.bold_white(args)}")

    asyncio.run(
        run_tasks(
            tasks.run(
                num_workers=args.num_workers,
                num_batches=args.num_batches,
                num_requests=args.num_requests,
                num_batches_per_worker=args.num_batches_per_worker,
                subnet_tag=args.subnet_tag,
                payment_driver=args.payment_driver,
                payment_network=args.payment_network,
            )
        )
    )
