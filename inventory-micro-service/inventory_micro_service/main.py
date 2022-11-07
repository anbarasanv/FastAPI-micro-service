from fastapi import FastAPI
from redis_om import get_redis_connection, HashModel
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*'],
)

redis = get_redis_connection(
    host="redis-14960.c305.ap-south-1-1.ec2.cloud.redislabs.com",
    port="14960",
    password="pkLQm5uLzlxFEEIRwHXi55NUxhhQKskP",
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
def get_all():
    return [product_format(pk) for pk in Product.all_pks()]


def product_format(prodct_pkey: str):
    product = Product.get(prodct_pkey)
    return {"id": product.pk,
            "name": product.name,
            "price": product.price,
            "quantity": product.quantity
            }


@app.post("/products")
def save_product(product: Product):
    return product.save()


@app.get("/products/{product_key}")
def get_single_product(product_key: str):
    return Product.get(product_key)


@app.delete("products/{pk}")
def delete_single_product(pk: str):
    return Product.delete(pk)