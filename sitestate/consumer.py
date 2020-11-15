import asyncio
import json
import logging

import asyncpg
from aiokafka import AIOKafkaConsumer

from sitestate import objects

CONSUMER_GROUP_ID = 'site_state_group_id'


class Consumer(object):
    def __init__(self, config):
        self.config = config
        self.pool = None
        self.consumer = None

    async def serve(self):
        """Starts consumer process."""
        self.pool = await asyncpg.create_pool(
            self.config.db.get_dsn())
        loop = asyncio.get_running_loop()
        kwargs = {'loop': loop, 'bootstrap_servers': self.config.kafka.hosts,
                  'group_id': CONSUMER_GROUP_ID}
        ssl_context = self.config.kafka.ssl_context()
        if ssl_context:
            kwargs['ssl_context'] = ssl_context
            kwargs['security_protocol'] = 'SSL'
        consumer = AIOKafkaConsumer(
            self.config.kafka.topic,
            **kwargs)
        await consumer.start()
        self.consumer = consumer
        loop.create_task(self._consume())

    async def _consume(self):
        """Consume records from kafka and writes it to db."""
        try:
            async for msg in self.consumer:
                data = json.loads(msg.value)
                logging.info('consumed: ', data)
                site_state = objects.SiteState(**data)
                await self._write_to_db(site_state)
        except Exception as e:
            logging.error('failed to process new message.', e)
        finally:
            await self.consumer.stop()

    async def _write_to_db(self, site_state):
        """DB update method for a site status."""
        async with self.pool.acquire() as db_conn:
            async with db_conn.transaction():
                await db_conn.execute(
                    '''INSERT INTO sitestate (url, regexp, has_text, code, ts)
                    VALUES ($1, $2, $3, $4, $5) ON CONFLICT (url)
                    DO UPDATE SET code = $4, ts=$5, has_text=$3''',
                    site_state.url, site_state.regexp, site_state.has_text,
                    site_state.code, site_state.timestamp)
