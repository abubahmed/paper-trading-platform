import redis

from core.config import settings

_client = redis.from_url(settings.redis_url, decode_responses=True)

ORDER_QUEUE = "order_queue"


def enqueue_order(order_id: str) -> None:
    """Push an order ID onto the left end of the order queue for the trading engine to consume."""
    _client.lpush(ORDER_QUEUE, order_id)
