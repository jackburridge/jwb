import asyncio
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer
from main import app


# start
@dataclass
class Operation:
    method: str
    path: str


async def run(app, bootstrap_servers, operations: dict[str, Operation]):
    consumer = AIOKafkaConsumer(bootstrap_servers=bootstrap_servers)
    consumer.subscribe(list(operations.keys()))
    await consumer.start()

    while True:
        async for consumer_record in consumer:
            operation = operations[consumer_record.topic]
            await handle_record(app, consumer_record, operation)


# end


async def handle_record(app, consumer_record, operation):
    # we will implement this later
    raise NotImplementedError


if __name__ == "__main__":
    asyncio.run(run(app, "localhost:9092", {"topic": Operation("POST", "/hello")}))
