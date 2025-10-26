import json
from csv import DictWriter
from urllib.parse import urlparse
from uuid import uuid4
from weakref import WeakValueDictionary

import gevent
from gevent import Timeout as GeventTimeout
from gevent.event import Event
from kafka import KafkaConsumer
from kafka import KafkaProducer
from locust import events
from locust import task
from locust import User


class KafkaListener:
    def __init__(self, bootstrap_servers):
        self.consumer = KafkaConsumer(
            "createOrder.reply", bootstrap_servers=bootstrap_servers
        )
        self.reply_events = WeakValueDictionary()

    def run(self):
        for message in self.consumer:
            for name, value in message.headers:
                if name == "x-request-id":
                    self.get_reply_event(value).set()
                    break

    def get_reply_event(self, request_id):
        return self.reply_events.setdefault(request_id, Event())


# request_record_file_start
@events.init_command_line_parser.add_listener
def _(parser):
    parser.add_argument(
        "--requests-record-file",
        type=str,
        default=None,
        help="CSV requests record file",
    )


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    environment.listener = KafkaListener(urlparse(environment.host).netloc)
    gevent.spawn(environment.listener.run)

    if environment.parsed_options.requests_record_file:
        request_record_csv = DictWriter(
            open(environment.parsed_options.requests_record_file, "w"),
            fieldnames=["request_type", "name", "response_time"],
        )

        request_record_csv.writeheader()

        @events.request.add_listener
        def _record_request(request_type, name, response_time, **kwargs):
            request_record_csv.writerow(
                {
                    "request_type": request_type,
                    "name": name,
                    "response_time": response_time,
                }
            )


# request_record_file_end


class Timeout(Exception):
    pass


class OrdersUser(User):
    def __init__(self, environment):
        super().__init__(environment)
        bootstrap_servers = urlparse(self.host).netloc
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.order = json.dumps({"items": [{"sku": "id-1234", "count": 1}]}).encode()

    @task
    def create_order(self):
        with self.environment.events.request.measure("KAFKA", "createOrder"):
            request_id = str(uuid4()).encode()
            reply_event = self.environment.listener.get_reply_event(request_id)
            self.producer.send(
                topic="createOrder",
                value=self.order,
                headers=[
                    ("reply-to", b"createOrder.reply"),
                    ("x-reply-set-header", b"x-request-id:" + request_id),
                ],
            )
            try:
                reply_event.wait(timeout=30)
            except GeventTimeout as e:
                # we have to wrap GeventTimeout as it is a BaseException and will not be caught by measure
                raise Timeout(str(e))
