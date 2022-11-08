import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)


# TODO: This should be updated to a different DB
redis = get_redis_connection(
    host="redis-14960.c305.ap-south-1-1.ec2.cloud.redislabs.com",
    port="14960",
    password="pkLQm5uLzlxFEEIRwHXi55NUxhhQKskP",
    decode_responses=True
)


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis


@app.post("/orders")
async def create_orders(request: Request):
    body = await request.json()
    req = requests.get(f'http://localhost:8000/products/{body.get("id")}')
    product = req.json()

    order = Order(
        product_id=body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    order_completed(order)
    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
