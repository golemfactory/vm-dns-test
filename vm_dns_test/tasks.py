import asyncio

import colorful
from datetime import datetime, timedelta, timezone
from functools import partial
from typing import List

from yapapi import Golem, Task

from script.dns_tester import NodeResults, ResultSummary

from . import package, strategy, utils, worker


async def run(
    num_workers, num_batches, num_requests, num_batches_per_worker, subnet_tag, max_batch_running_time = None, payment_driver=None, payment_network=None, quiet=False,
):
    start_time = datetime.now()
    summary = ResultSummary()

    async with Golem(
        budget=5.0,
        subnet_tag=subnet_tag,
        payment_driver=payment_driver,
        payment_network=payment_network,
        strategy=strategy.ScanStrategy(summary),
    ) as golem:
        if not quiet:
            utils.print_env_info(golem)
        dns_tester_args = ["-r", num_requests]
        if max_batch_running_time:
            dns_tester_args.extend(["-m", max_batch_running_time])

        completed_tasks = golem.execute_tasks(
            partial(
                worker.worker,
                summary=summary,
                dns_tester_args=dns_tester_args,
                max_tasks=num_batches_per_worker
            ),
            [Task(data=h) for h in range(num_batches)],
            payload=await package.get_package(),
            max_workers=num_workers,
            timeout=timedelta(hours=1),
        )
        try:
            async for task in completed_tasks:
                results: NodeResults = task.result
                if not quiet:
                    print(colorful.bold_cyan(f"{task.data}: {results.summary()}"))
        except asyncio.CancelledError:
            pass

    summary.running_time = int((datetime.now() - start_time).total_seconds())
    return summary
