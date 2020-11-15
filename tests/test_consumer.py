import unittest
from unittest import mock

from sitestate import consumer as cons
from sitestate import objects


class ConsumerTestCase(unittest.IsolatedAsyncioTestCase):

    async def test_watch(self):
        mock_msg = mock.MagicMock()
        mock_msg.value = '''
        {
            "url": "www.example.com",
            "regexp": "",
            "has_text": true,
            "code": 200,
            "timestamp": 1605513878.264538,
            "correlation_id": "cor_id"}'''
        mock_rcv = mock.AsyncMock()
        mock_rcv.__aiter__.return_value = [mock_msg]
        config = objects.ConsumerConfig(
            kafka={'hosts': ['host1'],
                   'topic': 'topic'},
            db={'host': 'host1',
                'user': 'user',
                'password': 'pass',
                'db_name': 'db1',
                'ssl_require': False}
        )
        consumer = cons.Consumer(config)
        consumer.consumer = mock_rcv
        consumer._write_to_db = mock.AsyncMock()
        await consumer._consume()
        self.assertEqual(1, consumer._write_to_db.await_count)
        self.assertEqual('www.example.com',
                         consumer._write_to_db.call_args[0][0].url)
