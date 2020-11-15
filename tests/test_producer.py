import json
import unittest
from unittest import mock
from unittest.mock import patch

from sitestate import objects
from sitestate import producer as prod


class ProducerTestCase(unittest.IsolatedAsyncioTestCase):

    @patch('aiohttp.ClientSession.get')
    async def test_watch(self, mock_get):
        config = objects.ProducerConfig(
                sites=[{'url': 'site1', 'regexp': None}],
                interval=2,
                kafka={'hosts': ['host1'],
                       'topic': 'topic',
                       'cafile': '1',
                       'certfile': '2',
                       'keyfile': '3'})
        producer = prod.Producer(config)
        status_code = 412
        mock_get.return_value.__aenter__.return_value.status = status_code
        producer.producer = mock.AsyncMock()
        await producer._watch(config.sites[0], 'topic')
        data = producer.producer.send_and_wait.call_args.kwargs['value']
        val = json.loads(data)
        self.assertEqual(status_code, val['code'])
