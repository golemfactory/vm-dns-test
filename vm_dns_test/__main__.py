import asyncio
import pathlib
from datetime import datetime, timedelta, timezone

from yapapi import Golem, Task, WorkContext
from yapapi.payload import vm
from yapapi.rest.activity import BatchTimeoutError

from yapapi.log import enable_default_logger

from . import worker, utils


async def main(
    subnet_tag, payment_driver=None, payment_network=None,
):
    package = await vm.repo(
        image_tag="golem/ray-on-golem:0.6.0-py3.10.13-ray2.7.1"
    )

    async with Golem(
        budget=1.0,
        subnet_tag=subnet_tag,
        payment_driver=payment_driver,
        payment_network=payment_network,
    ) as golem:
        utils.print_env_info(golem)

        num_tasks = 0
        start_time = datetime.now()

        completed_tasks = golem.execute_tasks(
            worker.worker,
            [Task(data=None)],
            payload=package,
            max_workers=3,
            timeout=timedelta(hours=1),
        )
        async for task in completed_tasks:
            num_tasks += 1
            print(
                f"Task done: {task}, result: {task.result}, time: {task.running_time}"
            )

        print(
            f"{num_tasks} tasks completed, total time: {datetime.now() - start_time}"
        )


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
        main(
            subnet_tag=args.subnet_tag,
            payment_driver=args.payment_driver,
            payment_network=args.payment_network,
        )
    )
