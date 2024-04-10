import pika

from ProjectUtils.MessagingService.queue_definitions import (
    channel,
    EXCHANGE_NAME,
    USER_QUEUE_ROUTING_KEY,
    WRAPPER_ZOOKING_ROUTING_KEY
)
from ProjectUtils.MessagingService.schemas import to_json, MessageFactory, MessageType
from UserService.schemas import UserBase, AvailableService, Service

# map from service name to its RabbitMQ routing key
service_to_routing_key = {
    AvailableService.ZOOKING: WRAPPER_ZOOKING_ROUTING_KEY
}


def publish_new_user(user: UserBase):
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=USER_QUEUE_ROUTING_KEY,
        body=to_json(MessageFactory.create_user_message(MessageType.USER_CREATE, user)),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )

def publish_import_properties(service: AvailableService, user: UserBase):
    routing_key = service_to_routing_key.get(service)
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=routing_key,
        body=to_json(MessageFactory.create_import_properties_message(user)),
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
        ),
    )