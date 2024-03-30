import pika

from ProjectUtils.MessagingService.queue_definitions import channel, EXCHANGE_NAME
from ProjectUtils.MessagingService.schemas import create_message, UserMessage, UserType
from ProjectUtils.MessagingService.user_schemas import UserBase


def publish_new_user(user: UserBase):
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key="",
        body=create_message(UserMessage(UserType.CREATE_USER, user)),
        properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE),
    )
