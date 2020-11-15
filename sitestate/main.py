import argparse
import asyncio
import logging
import os
import yaml

from sitestate import objects
from sitestate import consumer
from sitestate import producer

CONSUME = 'consume'
PRODUCE = 'produce'


def main():
    parser = argparse.ArgumentParser(prog='watcher')
    parser.add_argument('-c', dest='conf', metavar='conf.yaml', required=True,
                        help='configuration file')
    parser.add_argument('command',
                        choices=[CONSUME, PRODUCE],
                        help='command to execute')
    args = parser.parse_args()
    config_path = args.conf
    if not (os.path.exists(config_path)):
        logging.error('conf file %s not found. exiting...' % config_path)
        return 1
    try:
        with open(config_path) as f:
            config = yaml.load(f, Loader=yaml.CLoader)
    except Exception:
        logging.error('failed to load config file. %s ', config_path)
        return 1
    if not config:
        logging.error('failed to load config file. %s ', config_path)
        return 1
    if args.command == CONSUME:
        consumer_config = objects.ConsumerConfig(**config)
        worker = consumer.Consumer(consumer_config)
    elif args.command == PRODUCE:
        producer_config = objects.ProducerConfig(**config)
        worker = producer.Producer(producer_config)
    loop = asyncio.get_event_loop()
    loop.create_task(worker.serve())
    loop.run_forever()


if __name__ == '__main__':
    main()
