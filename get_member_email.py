#!/usr/bin/env python

from refreshbooks import api
import ConfigParser
import argparse
import pprint
import logging

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(
    description='Determine a client email address from a freshbooks recurring_id')
parser.add_argument('id', nargs='*',
                    help='freshbooks recurring_id to search for')
parser.add_argument('--config', '-c', dest='config',
                    default='/etc/freshbooks.cfg',
                    help='config file name (default: /etc/freshbooks.cfg)')

args = parser.parse_args()

config = ConfigParser.RawConfigParser()
config.read(args.config)

api_token = config.get('Freshbooks', 'api_token')

c = api.TokenClient(
    'iocoop.freshbooks.com',
    api_token,
    user_agent='get_member_email.py/1.0'
)

emails = {}

recurring_response = c.recurring.list()
logging.debug('total pages : %s' % recurring_response.recurrings.attrib['pages'])
for page in range(2, int(recurring_response.recurrings.attrib['pages']) + 2):
    for recurring in recurring_response.recurrings.recurring:
        logging.debug('recurring.recurring_id = %s' % recurring.recurring_id)
        logging.debug('recurring.stopped = %s' % recurring.stopped)

        for recurring_id in args.id:
            if str(recurring.recurring_id) == recurring_id:
                if recurring.recurring_id not in emails:
                    emails[recurring.recurring_id] = {}
                emails[recurring.recurring_id]['client_id'] = recurring.client_id
                emails[recurring.recurring_id]['recurring_stopped'] = recurring.stopped

    logging.debug('page %s' % page)
    recurring_response = c.recurring.list(page=page)

logging.debug('emails %s' % emails)


client_response = c.client.list()
logging.debug('total pages : %s' % client_response.clients.attrib['pages'])
for page in range(2, int(client_response.clients.attrib['pages']) + 2):
    for client in client_response.clients.client:
        logging.debug('client.email = %s' % client.email)
        if client.client_id in [x['client_id'] for x in emails.values()]:
            recurring_id = next(x for x in emails
                if emails[x]['client_id'] == client.client_id)
            emails[recurring_id]['email'] = client.email

    logging.debug('page %s' % page)
    client_response = c.client.list(page=page)
pprint.pprint(emails)
