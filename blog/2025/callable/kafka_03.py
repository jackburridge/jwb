import asyncio
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer
from main import app


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


# start
class Receive:
    def __init__(self, receive):
        self._receive = receive

    async def __call__(self):
        return self._receive


class Send:
    async def __call__(self, message):
        # we will implement this later
        pass


async def handle_record(app, consumer_record, operation):
    headers = [
        (name.lower().encode(), value) for name, value in consumer_record.headers
    ]
    scope = {
        "type": "http",
        "asgi": {"spec_version": "2.3", "version": "3.0"},
        "http_version": "1.1",
        "method": operation.method,
        "path": operation.path,
        "query_string": b"",
        "headers": headers,
    }
    receive = Receive(
        {
            "type": "http.request",
            "body": consumer_record.value or b"",
            "more_body": False,
        }
    )
    send = Send()

    await app(scope, receive, send)


# end

if __name__ == "__main__":
    asyncio.run(run(app, "localhost:9092", {"topic": Operation("POST", "/hello")}))
