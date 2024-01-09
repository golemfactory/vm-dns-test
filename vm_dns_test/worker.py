import pathlib
from yapapi import WorkContext

from script.dns_tester import Result


SCRIPT = pathlib.Path(__file__).resolve().parents[1] / "script" / "dns_tester.py"


async def worker(ctx: WorkContext, tasks):
    async for task in tasks:
        outputs = list()

        async def add_output(output):
            outputs.extend([Result(**o) for o in output])

        script = ctx.new_script()
        script.upload_file(SCRIPT, "/golem/dns_tester.py")
        script.run("/usr/local/bin/python", "/golem/dns_tester.py", "-o", "/golem/out.json")
        script.download_json("/golem/out.json", add_output)

        yield script

        task.accept_result(outputs)
