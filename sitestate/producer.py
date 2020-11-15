import asyncio
import json
import random
import time

import aiohttp
import aiokafka
import async_timeout


class Producer(object):
    def __init__(self, config):
        self.config = config
        self.producer = None

    async def serve(self):
        """Starts producer process."""
        loop = asyncio.get_running_loop()
        self.producer = await self._get_producer(loop)

        for site in self.config.sites:
            loop.create_task(
                self._watch_forever(site, self.config.interval,
                                    self.config.kafka.topic))
            # NOTE(tdurakov): do not spin all at the same moment
            await asyncio.sleep(random.randint(0, 1))

    async def _get_producer(self, loop):
        """Inits kafka producer."""
        kwargs = {'loop': loop, 'bootstrap_servers': self.config.kafka.hosts}
        ssl_context = self.config.kafka.ssl_context()
        if ssl_context:
            kwargs['ssl_context'] = ssl_context
            kwargs['security_protocol'] = 'SSL'
        producer = aiokafka.AIOKafkaProducer(
            **kwargs)
        await loop.create_task(producer.start())
        return producer

    async def _watch_forever(self, site_def, interval, topic):
        """Main producer loop."""
        while True:
            then = time.time()
            with async_timeout.timeout(interval):
                await self._watch(site_def, topic)
            elapsed = time.time() - then
            await asyncio.sleep(interval - elapsed)

    async def _watch(self, site_def, topic):
        """Get site http response and write it to kafka."""
        async with aiohttp.ClientSession() as session:
            async with session.get(site_def.url) as response:
                report = await site_def.get_report(response)
                await self.producer.send_and_wait(topic,
                                                  value=str.encode(
                                                      json.dumps(
                                                          report)),
                                                  key=str.encode(
                                                      site_def.url))
