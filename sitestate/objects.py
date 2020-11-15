import datetime
import re
import uuid

from aiokafka import helpers


class DBConfig(object):
    def __init__(self, host, user, password, db_name, ssl_require=True):
        self.host = host
        self.user = user
        self.password = password
        self.db_name = db_name
        self.ssl_require = ssl_require

    def get_dsn(self):
        return 'postgres://%s:%s@%s/%s%s' % (
            self.user, self.password, self.host, self.db_name,
            '?sslmode=require' if self.ssl_require else '')


class KafkaConfig(object):
    def __init__(self, hosts, topic, cafile=None, certfile=None, keyfile=None):
        self.hosts = hosts
        self.topic = topic
        self.cafile = cafile
        self.certfile = certfile
        self.keyfile = keyfile

    def ssl_context(self):
        if self.cafile and self.certfile and self.keyfile:
            return helpers.create_ssl_context(
                cafile=self.cafile,
                certfile=self.certfile,
                keyfile=self.keyfile)
        return None


class ProducerConfig(object):
    def __init__(self, sites, interval, kafka):
        self.sites = [Site(**site) for site in sites]
        self.interval = interval
        self.kafka = KafkaConfig(**kafka)


class ConsumerConfig(object):
    def __init__(self, kafka, db):
        self.kafka = KafkaConfig(**kafka)
        self.db = DBConfig(**db)


class Site(object):
    def __init__(self, url, regexp=None):
        self.url = url
        self.regexp = regexp
        if regexp:
            self.compiled_regexp = re.compile(regexp)

    async def get_report(self, response):
        has_text = True
        if self.regexp:
            text = await response.text()
            has_text = self.compiled_regexp.search(text) is not None
        return {
            'url': self.url,
            'regexp': self.regexp,
            'has_text': has_text,
            'code': response.status,
            'timestamp': datetime.datetime.utcnow().timestamp(),
            'correlation_id': str(uuid.uuid4())
        }


class SiteState(object):
    def __init__(self, url, regexp, has_text, code, timestamp, correlation_id):
        self.url = url
        self.regexp = regexp
        self.has_text = has_text
        self.code = code
        self.timestamp = datetime.datetime.utcfromtimestamp(timestamp)
        self.correlation_id = correlation_id
