from aio_pika import connect_robust, ExchangeType, Message

from ProjectUtils.MessagingService.queue_definitions import (
    channel,
    EXCHANGE_NAME,
    USER_QUEUE_NAME,
    USER_QUEUE_ROUTING_KEY,
    WRAPPER_ZOOKING_ROUTING_KEY,
    WRAPPER_CLICKANDGO_ROUTING_KEY,
    WRAPPER_EARTHSTAYIN_ROUTING_KEY,
    WRAPPER_BROADCAST_ROUTING_KEY
)
from ProjectUtils.MessagingService.schemas import to_json, MessageFactory, MessageType, to_json_aoi_bytes
from UserService.schemas import UserBase, AvailableService, Service

# map from service name to its RabbitMQ routing key
service_to_routing_key = {
    AvailableService.ZOOKING: WRAPPER_ZOOKING_ROUTING_KEY,
    AvailableService.CLICKANDGO: WRAPPER_CLICKANDGO_ROUTING_KEY,
    AvailableService.EARTHSTAYIN: WRAPPER_EARTHSTAYIN_ROUTING_KEY
}

channel.close()  # TODO: fix in the future

async_exchange = None


async def init_publisher(loop):
    connection = await connect_robust(host="rabbit_mq", loop=loop)

    global async_channel

    async_channel = await connection.channel()

    global async_exchange

    async_exchange = await async_channel.declare_exchange(
        name=EXCHANGE_NAME, type=ExchangeType.TOPIC, durable=True
    )

    users_queue = await async_channel.declare_queue(USER_QUEUE_NAME, durable=True)

    await users_queue.bind(exchange=EXCHANGE_NAME, routing_key=USER_QUEUE_ROUTING_KEY)

    return connection


async def publish_new_user(user: UserBase):
    global async_exchange

    await async_exchange.publish(
        routing_key=USER_QUEUE_ROUTING_KEY,
        message=to_json_aoi_bytes(MessageFactory.create_user_message(MessageType.USER_CREATE, user)),
    )


async def publish_import_properties(service: AvailableService, user: UserBase):
    global async_exchange

    routing_key = service_to_routing_key.get(service)

    await async_exchange.publish(
        routing_key=routing_key,
        message=to_json_aoi_bytes(MessageFactory.create_import_properties_message(user)),
    )

async def publish_import_reservations(users: list[UserBase]):
    global async_exchange
    await async_exchange.publish(
        routing_key=WRAPPER_BROADCAST_ROUTING_KEY,
        message=to_json_aoi_bytes(MessageFactory.create_import_reservations_message(users)),
    )

async def publish_scheduled_import_properties(users: list[UserBase]):
    global async_exchange
    await async_exchange.publish(
        routing_key=WRAPPER_BROADCAST_ROUTING_KEY,
        message=to_json_aoi_bytes(MessageFactory.create_scheduled_properties_import_message(users)),
    )