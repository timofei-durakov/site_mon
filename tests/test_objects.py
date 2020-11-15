import unittest
from unittest.mock import patch

from sitestate import objects


class ObjectsTestCase(unittest.TestCase):

    def test_db_config(self):
        db_conf = objects.DBConfig('host', 'user', 'pass', 'db_name')
        dsn = db_conf.get_dsn()
        assert 'postgres://user:pass@host/db_name?sslmode=require' == dsn

    @patch('aiokafka.helpers.create_ssl_context')
    def test_kafka_config(self, patched_ssl):
        kafka_conf = objects.KafkaConfig(['host1'], 'topic', 'cafile',
                                         'certfile', 'certkey')
        kafka_conf.ssl_context()
        patched_ssl.assert_called_once_with(cafile='cafile',
                                            certfile='certfile',
                                            keyfile='certkey')
