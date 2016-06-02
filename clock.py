#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import requests
import sys

from apscheduler.schedulers.blocking import BlockingScheduler


LOG = logging.getLogger(sys.argv[0])
ENDPOINT = 'https://groceries-api.herokuapp.com/status'


class Pinger(object):

    scheduler_class = BlockingScheduler

    def __init__(self, scheduler_class=None):
        if scheduler_class is not None:
            self.scheduler_class = scheduler_class
        logging.basicConfig(level=logging.INFO)
        scheduler = self.scheduler_class()
        scheduler.add_job(
            self.ping(ENDPOINT),
            trigger='interval',
            minutes=25)
        scheduler.start()

    def ping(self, url):
        def fn():
            LOG.info('Pinging {}'.format(url))
            return requests.get(url)
        return fn


if __name__ == '__main__': # pragma: no cover
    Pinger()
