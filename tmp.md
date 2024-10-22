我使用 `await asyncio.sleep(1)` 模拟函数耗时


我使用的python 3.11，请根据下列内容，给我一份耗时最少的python代码。

项目场景:

项目中有三个使用yield的异步生成器(第二、三个异步生成器很耗时)，第一个异步生成器每一次yield出的内容需要立刻进入第二个异步生成器，成为第二个异步生成器的参数。第二个异步生成器每一次yield出的内容需要立刻进入第三个异步生成器，成为第三个异步生成器的参数。

项目需要尽最大可能降低耗时。

我使用的python 3.11，我研究了下`asyncio`，我发现`asyncio.TaskGroup`、`asyncio.gather`、`asyncio.wait`都是在并行化同时运行多个互不相关的任务，是这样吗？


我使用的python 3.12，我的代码逻辑如下。怎样才能优化下列代码，减少耗时。

```python
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
```