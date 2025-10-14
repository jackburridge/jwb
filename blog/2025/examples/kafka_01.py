import asyncio

from aiokafka import AIOKafkaConsumer
from main import app


def run(app, bootstrap_servers):
    asyncio.run(run_async(app, bootstrap_servers))


async def run_async(app, bootstrap_servers):
    consumer = AIOKafkaConsumer(bootstrap_servers=bootstrap_servers)
    await consumer.start()

    async for consumer_record in consumer:
        await handle_record(app, consumer_record)


async def handle_record(app, consumer_record):
    # we will implement this later
    raise NotImplementedError


if __name__ == "__main__":
    run(app, "localhost:9092")
