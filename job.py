
import redis

from rq import Queue

try:
    r = redis.Redis()
except Exception:
    r = redis.Redis(host='redis', port=6379)
q = Queue(connection=r, is_async=False)


