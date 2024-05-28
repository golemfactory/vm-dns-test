import colorful
from datetime import datetime
import json
import pathlib
from typing import List
from yapapi import WorkContext

from script.dns_tester import Node, NodeResults, Result, ResultSummary


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "script" / "dns_tester.py"
SCRIPT_CONTENTS = open(SCRIPT, "rb").read()


async def worker(ctx: WorkContext, tasks, dns_tester_args: List, summary: ResultSummary, max_tasks = 1):
    dns_tester_args = [str(a) for a in dns_tester_args]

    task_cnt = 0

    script = ctx.new_script()
    script.upload_bytes(SCRIPT_CONTENTS, "/golem/dns_tester.py")
    yield script

    async for task in tasks:
        task_cnt += 1
        node = Node.get_node_by_id(ctx.provider_id)
        node.name = ctx.provider_name

        start_time = datetime.now()

        outputs = list()

        async def get_output(output):
            outputs.extend([Result(**o) for o in output])

        script = ctx.new_script()
        script.run(
            "/usr/local/bin/python",
            "/golem/dns_tester.py",
            "-o",
            "/golem/out.json",
            *dns_tester_args
        )
        script.download_json("/golem/out.json", get_output)

        yield script

        run_results = summary.add(node, outputs)
        run_results.running_time = int((datetime.now() - start_time).total_seconds())
        task.accept_result(run_results)

        if task_cnt >= max_tasks:
            await tasks.aclose()
