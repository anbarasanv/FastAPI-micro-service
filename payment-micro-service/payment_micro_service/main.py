from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests
import time


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


@app.get('/orders')
def get_order():
    return [Order.get(pk) for pk in Order.all_pks()]


@app.get('/orders/{order_key}')
def get_order(order_key: str):
    return Order.get(order_key)


@app.post("/orders")
async def create_orders(request: Request, background_tasks: BackgroundTasks):
    body = await request.json()
    req = requests.get(f'http://localhost:8000/products/{body.get("id")}')
    product = req.json()

    order = Order(
        product_id=body['id'],
        name=product['name'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    background_tasks.add_task(order_completed, order)
    return order


def order_completed(order: Order):
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')


@app.delete("/orders/{order_key}")
def delete_order(order_key: str):
    return Order.delete(order_key)
