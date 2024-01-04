from yapapi.rest.activity import BatchTimeoutError
from yapapi import WorkContext


async def worker(ctx: WorkContext, tasks):

    async for task in tasks:
        script = ctx.new_script()
        try:
            yield script
            task.accept_result()
        except BatchTimeoutError:
            print(
                f"Task {task} timed out on {ctx.provider_name}, time: {task.running_time}"
            )
            raise
