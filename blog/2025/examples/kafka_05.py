import asyncio
from dataclasses import dataclass

from aiokafka import AIOKafkaConsumer
from aiokafka import AIOKafkaProducer
from main import app


@dataclass
class Operation:
    method: str
    path: str


def run(app, bootstrap_servers, operations):
    asyncio.run(run_async(app, bootstrap_servers, operations))


# run_start
async def run_async(app, bootstrap_servers, operations):
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
class Send:
    def __init__(self):
        self._send_queue = asyncio.Queue()

    async def __call__(self, message):
        self._send_queue.put_nowait(message)

    async def get(self):
        return await self._send_queue.get()


async def handle_send(producer, reply_topic, send):
    http_response_start = await send.get()
    assert http_response_start["type"] == "http.response.start"
    headers = http_response_start["headers"]
    status_code = http_response_start["status"]
    body = b""
    more_body = True
    while more_body:
        http_response_body = await send.get()
        assert http_response_body["type"] == "http.response.body"
        body += http_response_body["body"]
        more_body = http_response_body.get("more_body", False)

    send_headers = [
        ("status-code", str(status_code).encode()),
        *((name.decode(), value) for name, value in headers),
    ]
    await producer.send_and_wait(
        reply_topic,
        body,
        headers=send_headers,
    )


# handle_send_end


# extract_reply_topic_from_headers_start


def extract_reply_topic_from_headers(headers):
    for name, value in headers:
        if name.lower() == "reply-to":
            return value.decode()
    return None


async def handle_record(app, consumer_record, operation, producer):
    reply_topic = extract_reply_topic_from_headers(consumer_record.headers)
    if reply_topic is None:  # we have nowhere to send to
        return

    # extract_reply_topic_from_headers_end
    scope = create_scope_from_record_and_operation(consumer_record, operation)
    receive = create_receive_from_record(consumer_record)
    send = Send()

    await asyncio.gather(
        app(scope, receive, send), handle_send(producer, reply_topic, send)
    )


if __name__ == "__main__":
    run(app, "localhost:9092", {"topic": Operation("POST", "/hello")})
