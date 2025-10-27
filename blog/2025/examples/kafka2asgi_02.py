import asyncio
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer
from main import app


# start
@dataclass
class Operation:
    method: str
    path: str


def run(app, bootstrap_servers, operations):
    asyncio.run(run_async(app, bootstrap_servers, operations))


async def run_async(app, bootstrap_servers, operations):
    consumer = AIOKafkaConsumer(bootstrap_servers=bootstrap_servers)
    consumer.subscribe(list(operations.keys()))
    await consumer.start()

    async for consumer_record in consumer:
        operation = operations[consumer_record.topic]
        await handle_record(app, consumer_record, operation)


async def handle_record(app, consumer_record, operation):
    # we will implement this later
    raise NotImplementedError


if __name__ == "__main__":
    run(app, "localhost:9092", {"example_topic": Operation("POST", "/hello")})
