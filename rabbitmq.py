import asyncio
import pika
import aio_pika
import pickle

from loguru import logger
from typing import Iterable, Any
from abc import ABC, abstractmethod
from aio_pika.message import AbstractIncomingMessage, Message
from pika.exceptions import AMQPError

class MQClient(ABC):
    def __init__(self, queue, url=None, exchange="", exchange_type=""):
        self.exchange = exchange
        self.queue = queue
        self.exchange_type = self.validate_exc_type(exchange_type)

        self._url = url or "amqp://guest:guest@localhost/"

    @staticmethod
    def validate_exc_type(exchange_type):
        if exchange_type == "":
            return "direct"

        if exchange_type.casefold() not in ("direct", "fanout", "topic"):
            raise AMQPError

        return exchange_type

    @staticmethod
    def to_bytes(obj):
        return pickle.dumps(obj)

    @staticmethod
    def from_bytes(obj):
        return pickle.loads(obj)

    @abstractmethod
    def on_message(self, *args, **kwargs):
        ...

    @abstractmethod
    def consumer(self, *args, **kwargs):
        ...

    @abstractmethod
    def consume_messages(self, *args, **kwargs):
        ...

    @abstractmethod
    def publish_message(self, *args, **kwargs):
        ...

    @abstractmethod
    def publish_messages(self, *args, **kwargs):
        ...

class MQAsyncClient(MQClient):
    def __init__(self, queue, url=None, exchange="", exchange_type=""):
        super().__init__(queue, url, exchange, exchange_type)

    @staticmethod
    async def on_message(message: AbstractIncomingMessage):
        async with message.process():
            print (" [x] Received message %r" % message)
            print (f"Decode message body is: {MQClient.from_bytes(message.body)}")

    async def consumer(self, callback=None):
        async def consume():
            nonlocal callback
            connection = await aio_pika.connect_robust(self._url)
            async with connection:
                channel = await connection.channel()
                try:
                    queue = await channel.get_queue(
                        name=self.queue,
                        ensure=True
                    )
                except (AMQPError,) as e:
                    logger.error(f"Failed to connect to queue: {e}")
                    raise AMQPError("Check queue in RabbitMQ. Failed with connect to this.")

                if callback is None:
                    callback = self.on_message

                await queue.consume(callback=callback)
                await asyncio.Future()

        task = asyncio.create_task(consume())
        return task

    async def consume_messages(self):
        connection = await aio_pika.connect_robust(self._url)
        async with connection:
            channel = await connection.channel()
            try:
                queue = await channel.get_queue(
                    name=self.queue,
                    ensure=True
                )
            except (AMQPError,) as e:
                logger.error(f"Failed to connect to queue: {e}")
                raise AMQPError("Check queue in RabbitMQ. Failed with connect to this.")

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        yield self.from_bytes(message.body)

    async def publish_message(self, message: Any):
        return await self.__publish(message)

    async def publish_messages(self, messages: Iterable):
        return await self.__publish(tuple(messages))

    async def __publish(self, data):
        connection = await aio_pika.connect_robust(self._url)
        async with connection:
            channel = await connection.channel()
            try:
                queue = await channel.get_queue(
                    name=self.queue,
                    ensure=True
                )
            except (AMQPError,) as _e:
                logger.error(f"Failed to connect to queue: {_e}")
                raise AMQPError("Check queue in RabbitMQ. Failed with connect to this.")

            if self.exchange == "":
                exchange = channel.default_exchange
            else:
                try:
                    exchange = await channel.get_exchange(name=self.exchange, ensure=True)
                except (AMQPError,) as e:
                    logger.error(f"Failed connect to exchange: {e}")
                    raise AMQPError("Check exchange in RabbitMQ. Failed with connect to this.")

            if isinstance(data, (tuple,)):
                for item in data:
                    await exchange.publish(
                        message=Message(
                            body=self.to_bytes(item)
                        ),
                        routing_key=queue.name
                    )
            elif isinstance(data, dict):
                await exchange.publish(
                    message=Message(
                        body=self.to_bytes(data)
                    ),
                    routing_key=queue.name
                )

class MQSyncClient(MQClient):
    def __init__(self, queue, url=None, exchange="", exchange_type=""):
        super().__init__(queue, url, exchange, exchange_type)
        self.connection = pika.BlockingConnection(pika.URLParameters(self._url))
        self.channel = self.connection.channel()

    @staticmethod
    def on_message(channel, method, properties, body):
        print(" [x] Received message %r" % body)
        print("Decode message body is: %r" % MQClient.from_bytes(body))
        channel.basic_ack(delivery_tag=method.delivery_tag)

    def consumer(self, callback=None):
        if callback is None:
            callback = self.on_message

        self.channel.basic_consume(queue=self.queue, on_message_callback=callback)
        self.channel.start_consuming()

    def consume_messages(self):
        for method, properties, body in self.channel.consume(self.queue):
            yield self.from_bytes(body)
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

    def publish_message(self, message):
        self.__publish(message)

    def publish_messages(self, messages: Iterable):
        self.__publish(tuple(messages))

    def __publish(self, data):
        if self.exchange == "":
            exchange = ""
        else:
            exchange = self.exchange

        if isinstance(data, (tuple, list,)):
            for item in data:
                self.channel.basic_publish(
                    exchange=exchange,
                    routing_key=self.queue,
                    body=self.to_bytes(item)
                )
        else:
            self.channel.basic_publish(
                exchange=exchange,
                routing_key=self.queue,
                body=self.to_bytes(data)
            )

    def close(self):
        self.connection.close()
