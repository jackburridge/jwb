from dataclasses import dataclass
from uuid import uuid4

import kafka_05 as kafka2asgi
from echo_set_header import EchoSetHeader
from fastapi import FastAPI
from kafka_05 import Operation


# start
app = FastAPI()


@dataclass
class Item:
    sku: str
    count: int


@dataclass
class Order:
    items: list[Item]


@app.post("/orders", operation_id="createOrder")
def create_order(order: Order):
    # fake API for this example
    return {"id": str(uuid4()), "items": order.items}


app.add_middleware(EchoSetHeader, echo_set_header="x-reply-set-header")

if __name__ == "__main__":
    kafka2asgi.run(
        app,
        bootstrap_servers="localhost:9092",
        operations={"createOrder": Operation("POST", "/orders")},
    )
