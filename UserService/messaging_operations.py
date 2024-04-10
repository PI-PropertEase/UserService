import pika

from ProjectUtils.MessagingService.queue_definitions import (
    channel,
    EXCHANGE_NAME,
    USER_QUEUE_ROUTING_KEY,
)
from ProjectUtils.MessagingService.schemas import to_json, MessageFactory, MessageType
from UserService.schemas import UserBase


def publish_new_user(user: UserBase):
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=USER_QUEUE_ROUTING_KEY,
        body=to_json(MessageFactory.create_user_message(MessageType.USER_CREATE, user)),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )
