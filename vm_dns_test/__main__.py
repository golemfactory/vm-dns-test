import asyncio
import colorful
from datetime import timedelta
from typing import Awaitable

from yapapi.log import enable_default_logger

from . import tasks, utils

from script.dns_tester import ResultSummary


if __name__ == "__main__":
    parser = utils.argument_parser()
    parser.add_argument("-w", "--num-workers", type=int, help="Number of concurrent workers. default=%(default)s", default=16)
    parser.add_argument("-b", "--num-batches", type=int, help="Overall number of batches/tasks to run. default=%(default)s", default=1024)
    parser.add_argument("-r", "--num-requests", type=int, help="Number of requests per batch. default=%(default)s", default=1024)
    parser.add_argument("-t", "--num-batches-per-worker", type=int, help="Number of batches (tasks) per a single worker run. default=%(default)s", default=1024)
    parser.add_argument("-m", "--max-batch-running-time", type=int, help="Maximum time for a single batch to run (seconds). default=%(default)s", default=int(timedelta(minutes=1).total_seconds()))
    args = parser.parse_args()

    enable_default_logger(
        log_file=args.log_file,
        debug_activity_api=True,
        debug_market_api=True,
        debug_payment_api=True,
        debug_net_api=True,
    )

    def run_tasks(run: Awaitable):
        loop = asyncio.get_event_loop()
        task = loop.create_task(run)

        try:
            loop.run_until_complete(task)
        except KeyboardInterrupt:
            print("Shutting down...")
            task.cancel()
            try:
                loop.run_until_complete(task)
                print("Shutdown completed.")
            except (asyncio.CancelledError, KeyboardInterrupt):
                pass

        summary: ResultSummary = task.result()
        print(summary.summary())

    print(f"Run arguments: {colorful.bold_white(args.__dict__)}")

    run_tasks(
        tasks.run(
            num_workers=args.num_workers,
            num_batches=args.num_batches,
            num_requests=args.num_requests,
            num_batches_per_worker=args.num_batches_per_worker,
            max_batch_running_time=args.max_batch_running_time,
            subnet_tag=args.subnet_tag,
            payment_driver=args.payment_driver,
            payment_network=args.payment_network,
        )
    )
