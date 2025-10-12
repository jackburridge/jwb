import asyncio
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer
from main import app


@dataclass
class Operation:
    method: str
    path: str


# run_start
async def run(app, bootstrap_servers, operations):
    consumer = AIOKafkaConsumer(bootstrap_servers=bootstrap_servers)
    producer = AIOKafkaProducer(bootstrap_servers=bootstrap_servers)
    consumer.subscribe(list(operations.keys()))
    await consumer.start()
    await producer.start()

    async for consumer_record in consumer:
        operation = operations[consumer_record.topic]
        await handle_record(app, consumer_record, operation, producer)


# run_end


class Receive:
    def __init__(self, receive):
        self._receive = receive

    async def __call__(self):
        return self._receive


class Send:
    async def __call__(self, message):
        # we will implement this later
        pass


def create_scope_from_record_and_operation(consumer_record, operation):
    headers = [
        (name.lower().encode(), value) for name, value in consumer_record.headers
    ]
    return {
        "type": "http",
        "asgi": {"spec_version": "2.3", "version": "3.0"},
        "http_version": "1.1",
        "method": operation.method,
        "path": operation.path,
        "query_string": b"",
        "headers": headers,
    }


def create_receive_from_record(consumer_record):
    return Receive(
        {
            "type": "http.request",
            "body": consumer_record.value or b"",
            "more_body": False,
        }
    )


# handle_send_start
async def handle_send(producer, send_topic, send):
    # we will implement this later
    pass


async def handle_record(app, consumer_record, operation, producer):
    reply_topic = None  # we will implement this next
    scope = create_scope_from_record_and_operation(consumer_record, operation)
    receive = create_receive_from_record(consumer_record)
    send = Send()

    await asyncio.gather(
        app(scope, receive, send), handle_send(producer, reply_topic, send)
    )


# handle_send_end

if __name__ == "__main__":
    asyncio.run(run(app, "localhost:9092", {"topic": Operation("POST", "/hello")}))
