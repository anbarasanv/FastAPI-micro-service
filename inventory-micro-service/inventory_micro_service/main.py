from fastapi import FastAPI
from redis_om import get_redis_connection


app = FastAPI()

redis = get_redis_connection(
    host="redis-14960.c305.ap-south-1-1.ec2.cloud.redislabs.com",
    port="14960",
    password="pkLQm5uLzlxFEEIRwHXi55NUxhhQKskP",
    decode_responses=True
)


@app.get("/")
async def root():
    return {"message": "Hello!"}