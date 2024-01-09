from datetime import datetime, timedelta, timezone
from typing import List

from yapapi import Golem, Task

from script.dns_tester import Result, ResultSummary

from . import package, utils, worker


async def run_tasks(
    subnet_tag, payment_driver=None, payment_network=None,
):

    summary = ResultSummary()

    async with Golem(
        budget=1.0,
        subnet_tag=subnet_tag,
        payment_driver=payment_driver,
        payment_network=payment_network,
    ) as golem:
        utils.print_env_info(golem)
        completed_tasks = golem.execute_tasks(
            worker.worker,
            [Task(data=None)],
            payload=await package.get_package(),
            max_workers=3,
            timeout=timedelta(hours=1),
        )
        async for task in completed_tasks:
            results: List[Result] = task.result
            print(results)


