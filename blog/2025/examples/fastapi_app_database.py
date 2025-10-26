from uuid import uuid4

import kafka_06 as kafka2asgi
import redis.asyncio as redis
from echo_set_header import EchoSetHeader
from fastapi import FastAPI
from kafka_06 import Operation
from pydantic import BaseModel


app = FastAPI()


class Item(BaseModel):
    sku: str
    count: int


class Order(BaseModel):
    items: list[Item]


client = redis.Redis(port=6666)


@app.post("/orders", operation_id="createOrder")
async def create_order(order: Order):
    id_uuid = uuid4()
    order_dict = order.model_dump()
    await client.json().set(f"order:{id_uuid}", "$", order_dict)
    return {"id": str(id_uuid), **order_dict}


app.add_middleware(EchoSetHeader, echo_set_header="x-reply-set-header")

if __name__ == "__main__":
    kafka2asgi.run(
        app,
        bootstrap_servers="localhost:9092",
        operations={"createOrder": Operation("POST", "/orders")},
    )
