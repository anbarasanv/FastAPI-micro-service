from main import redis, Order
import time


key = 'refund_order'
group = 'order-group'

try:
    redis.xgroup_create(key, group)
except Exception as e:
    print(f'Group is already exists!')

while True:
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
        if results:
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj.get('pk'))
                print(order)
                order.status = 'refunded'
                order.save()
    except Exception as e:
        print(str(e))
    time.sleep(1)
