import asyncio

async def worker(n):
    await asyncio.sleep(1)
    print(f"Worker {n} 完成")
    return n

async def task_generator():
    for i in range(5):
        yield asyncio.create_task(worker(i))

async def main():
    tasks = [task async for task in task_generator()]
    done, pending = await asyncio.wait(tasks)
    for task in done:
        print(f"结果: {task.result()}")

asyncio.run(main())
