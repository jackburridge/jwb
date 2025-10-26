import json
from urllib.parse import urlparse

from kafka import KafkaProducer
from locust import task
from locust import User


class OrdersUser(User):
    def __init__(self, environment):
        super().__init__(environment)
        bootstrap_servers = urlparse(self.host).netloc
        self.producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
        self.order = json.dumps({"items": [{"sku": "id-1234", "count": 1}]}).encode()

    @task
    def create_order(self):
        with self.environment.events.request.measure("KAFKA", "createOrder"):
            self.producer.send(
                topic="createOrder",
                value=self.order,
                headers=[("reply-to", b"createOrder.reply")],
            )
