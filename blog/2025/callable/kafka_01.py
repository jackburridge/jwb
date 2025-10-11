import asyncio

from aiokafka import AIOKafkaConsumer
from main import app


async def run(app, bootstrap_servers):
    consumer = AIOKafkaConsumer(bootstrap_servers=bootstrap_servers)
    await consumer.start()

    async for consumer_record in consumer:
        await handle_record(app, consumer_record)


async def handle_record(app, consumer_record):
    # we will implement this later
    raise NotImplementedError


if __name__ == "__main__":
    asyncio.run(run(app, "localhost:9092"))
