from dataclasses import dataclass
from uuid import uuid4

import uvicorn
from echo_set_header import EchoSetHeader
from fastapi import FastAPI

app = FastAPI()


@dataclass
class Order:
    skus: list[str]


@app.post("/orders")
def create_order(order: Order):
    return {"id": str(uuid4()), "skus": order.skus}


app.add_middleware(EchoSetHeader)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
