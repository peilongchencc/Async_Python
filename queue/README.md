# 异步队列 asyncio.Queue

`asyncio.Queue` 是 Python 的异步任务调度库 `asyncio` 中的一个类，专门用于在协程之间进行线程安全的队列通信。它允许多个生产者和多个消费者之间传递消息或数据，而不必担心数据竞争问题。`asyncio.Queue` 可以用于在异步任务之间高效、安全地共享数据。
- [异步队列 asyncio.Queue](#异步队列-asyncioqueue)
  - [1. 创建队列](#1-创建队列)
  - [2. 队列操作](#2-队列操作)
    - [示例：生产者-消费者模型](#示例生产者-消费者模型)
  - [3. `put_nowait()` 和 `get_nowait()`](#3-put_nowait-和-get_nowait)
    - [示例：`put_nowait` 和 `get_nowait`](#示例put_nowait-和-get_nowait)
    - [阻塞 vs 非阻塞操作](#阻塞-vs-非阻塞操作)
  - [4. 队列的属性和方法补充](#4-队列的属性和方法补充)
    - [示例：队列属性](#示例队列属性)
  - [5. `task_done()` 和 `join()`](#5-task_done-和-join)
    - [示例：等待队列处理完所有项目](#示例等待队列处理完所有项目)
  - [总结](#总结)


下面详细介绍 `asyncio.Queue` 的关键概念和使用方法。

## 1. 创建队列

要创建一个 `asyncio.Queue`，只需指定可选的 `maxsize` 参数，该参数定义了队列的最大长度。**如果 maxsize 未被指定，队列的大小会被认为是“无限”的，也就是队列不会被认为“满了”，直到系统内存耗尽。**

```python
import asyncio

queue = asyncio.Queue(maxsize=10)  # 创建一个最大容量为 10 的队列
```


## 2. 队列操作

- `put(item)`：将一个项目放入队列。如果队列已满，`put()` 将阻塞，直到有空间可用。

- `get()`：从队列中取出一个项目。如果队列为空，`get()` 将阻塞，直到有项目可取。

### 示例：生产者-消费者模型

```python
import asyncio

async def producer(queue):
    for i in range(5):
        await asyncio.sleep(1)  # 模拟生产数据的过程
        await queue.put(i)  # 将数据放入队列
        print(f'Produced {i}')

async def consumer(queue):
    while True:
        item = await queue.get()  # 从队列中获取数据
        print(f'Consumed {item}')
        queue.task_done()  # 标记队列任务完成
        if item == 4:  # 消费特定数据后退出
            break

async def main():
    queue = asyncio.Queue()
    # 同时运行生产者和消费者
    await asyncio.gather(producer(queue), consumer(queue))

asyncio.run(main())
```


## 3. `put_nowait()` 和 `get_nowait()`

这两个方法分别是 `put()` 和 `get()` 的非阻塞版本。

- **`put_nowait(item)`**：立即将 `item` 放入队列中。如果队列已满，抛出 `queue.Full` 异常。

- **`get_nowait()`**：立即从队列中获取项目。如果队列为空，抛出 `queue.Empty` 异常。

### 示例：`put_nowait` 和 `get_nowait`

```python
import asyncio
from asyncio import Queue

queue = Queue(maxsize=2)

# put_nowait 如果队列满了会抛出异常
try:
    queue.put_nowait(1)
    queue.put_nowait(2)
    queue.put_nowait(3)  # 这里会抛出 queue.Full 异常
except asyncio.QueueFull:
    print("Queue is full!")

# get_nowait 如果队列为空会抛出异常
try:
    item = queue.get_nowait()
    print(f'Got {item}')
    queue.get_nowait()  # 这里会正常运行
    queue.get_nowait()  # 这里会抛出 queue.Empty 异常
except asyncio.QueueEmpty:
    print("Queue is empty!")
```

### 阻塞 vs 非阻塞操作

`asyncio.Queue` 提供的 `put()` 和 `get()` 是阻塞操作，它们会在队列满或空的情况下等待，而 `put_nowait()` 和 `get_nowait()` 是非阻塞的，立即返回结果或抛出异常。


## 4. 队列的属性和方法补充

- **`empty()`**：如果队列为空，返回 `True`。

- **`full()`**：如果队列已满，返回 `True`。

- **`qsize()`**：返回队列中当前项目的数量。

### 示例：队列属性

```python
import asyncio

async def check_queue():
    queue = asyncio.Queue(maxsize=2)

    # 插入项目
    await queue.put(1)
    await queue.put(2)

    # 检查队列是否满了
    if queue.full():
        print("Queue is full!")

    # 获取队列大小
    print(f"Queue size: {queue.qsize()}")

    # 获取并移除项目
    await queue.get()
    await queue.get()
    if queue.empty():
        print("Queue is empty!")

# 运行异步函数
asyncio.run(check_queue())
```


## 5. `task_done()` 和 `join()`

- `task_done()`：通知队列某个 `get()` 操作已经完成。每个 `get()` 之后都应该调用 `task_done()`，否则 `join()` 将永远不会结束。

- `join()`：阻塞，直到所有通过 `put()` 放入队列的项目都被 `task_done()` 标记为已处理。

### 示例：等待队列处理完所有项目

```python
import asyncio

async def producer(queue):
    for i in range(5):
        await queue.put(i)
        print(f'Produced {i}')

async def consumer(queue):
    while True:
        item = await queue.get()
        print(f'Consumed {item}')
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    consumer_task = asyncio.create_task(consumer(queue))  # 创建消费者任务
    await producer(queue)  # 生产者完成生产任务
    await queue.join()  # 等待队列中的所有项目被处理
    consumer_task.cancel()  # 生产完成后，取消消费者任务

asyncio.run(main())
```

注意：队列本身没有 `cancel()` 方法，但 `asyncio.Queue` 通常和 `asyncio.Task` 一起使用，任务是可以取消的。当你不再需要消费者任务时，你可以调用 `task.cancel()` 来取消正在运行的任务。


## 总结

`asyncio.Queue` 作为异步编程中的核心组件，能够有效地处理生产者和消费者之间的任务调度。通过使用阻塞和非阻塞方法、任务取消机制以及队列状态监控，你可以实现高度并发和复杂任务处理的系统。
