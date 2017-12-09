#!/usr/bin/env python

from refreshbooks import api
import ConfigParser
import argparse
import pprint
import logging

logging.basicConfig(level=logging.INFO)

TERMS = 'IO Cooperative Terms of Service can be found at https://iocoop.org/policies/terms-of-service which includes by reference our billing policy which can be found at https://iocoop.org/policies/billing-policy'

parser = argparse.ArgumentParser(description='Update the terms of all non-stopped recurring invoices')
parser.add_argument('--config', '-c', dest='config', default='/etc/freshbooks.cfg',
                   help='config file name (default: /etc/freshbooks.cfg)')

args = parser.parse_args()

config = ConfigParser.RawConfigParser()
config.read(args.config)

api_token = config.get('Freshbooks', 'api_token')

c = api.TokenClient(
    'iocoop.freshbooks.com',
    api_token,
    user_agent='update_recurring_terms.py/1.0'
)

recurring_response = c.recurring.list()
logging.debug('total pages : %s' % recurring_response.recurrings.attrib['pages'])
for page in range(2, int(recurring_response.recurrings.attrib['pages']) + 2):
    for recurring in recurring_response.recurrings.recurring:
        logging.debug('recurring.recurring_id = %s' % recurring.recurring_id)
        logging.debug('recurring.stopped = %s' % recurring.stopped)
        if recurring.stopped == 0:
            print('##### %s #####' % recurring.recurring_id)
            print(recurring.terms)
            update_response = c.recurring.update(
                recurring=dict(
                    recurring_id=recurring.recurring_id,
                    terms=TERMS
                )
            )
            print("%s %s" % (recurring.recurring_id, update_response.get('status')))
            print('#############')
    logging.debug('page %s' % page)
    recurring_response = c.recurring.list(page=page)
