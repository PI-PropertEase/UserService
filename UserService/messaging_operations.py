import json
import pika

from ProjectUtils.MessagingService.queue_definitions import channel, EXCHANGE_NAME
from UserService.schemas import UserBase


def publish_new_user(user: UserBase):
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key="",
        body=json.dumps({"type": "new_user", "email": user.email}),
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
    )
