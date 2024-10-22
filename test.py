import time
import asyncio

async def generator1():
    """模拟音频流
    """
    for i in range(1, 6):
        await asyncio.sleep(1)
        yield i

async def generator2():
    """模拟大模型处理
    """
    async for value in generator1():
        await asyncio.sleep(1)
        yield value ** 2

async def generator3():
    """模拟大模型返回的chunk转语音
    """
    async for value in generator2():
        await asyncio.sleep(1)
        yield str(value)

async def main():
    start_time = time.time()  # 记录开始时间
    async for value in generator3():
        print(value, type(value))
    
    end_time = time.time()  # 记录结束时间
    print(f"总体执行时长: {end_time - start_time:.2f}秒")

# 运行主函数
asyncio.run(main())
