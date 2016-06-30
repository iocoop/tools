#!/usr/bin/env python

from refreshbooks import api
import ConfigParser
import argparse
import pprint
import logging

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Audit recurring profile line items')
parser.add_argument('--config', '-c', dest='config', default='/etc/freshbooks.cfg',
                   help='config file name (default: /etc/freshbooks.cfg)')

args = parser.parse_args()

config = ConfigParser.RawConfigParser()
config.read(args.config)

api_token = config.get('Freshbooks', 'api_token')

c = api.TokenClient(
    'iocoop.freshbooks.com',
    api_token,
    user_agent='audit_recurring_line_items.py/1.0'
)




clients = {}
client_response = c.client.list()
logging.debug('total pages : %s' % client_response.clients.attrib['pages'])
for page in range(2, int(client_response.clients.attrib['pages']) + 2):
    for client in client_response.clients.client:
        logging.debug('client.email = %s' % client.email)
        clients[client.client_id] = client
    logging.debug('page %s' % page)
    client_response = c.client.list(page=page)

recurring_response = c.recurring.list()
logging.debug('total pages : %s' % recurring_response.recurrings.attrib['pages'])
for page in range(2, int(recurring_response.recurrings.attrib['pages']) + 2):
    for recurring in recurring_response.recurrings.recurring:
        logging.debug('recurring.recurring_id = %s' % recurring.recurring_id)
        logging.debug('recurring.stopped = %s' % recurring.stopped)
        if recurring.stopped == 0:
            #logging.info("%s: %s '%s' '%s %s'" % (recurring.recurring_id, , clients[recurring.client_id], recurring.organization, recurring.first_name, recurring.last_name))
            #logging.info("%s" % clients[recurring.client_id].email)
            for line in recurring.lines.line:
                if '-GNT-' in str(line.name):
                    print '"%s", "%s", "%s", "%s", "%s %s", "%s"' % (
                        recurring.recurring_id,
                        line.name,
                        line.unit_cost,
                        str(clients[recurring.client_id].email).lower(),
                        clients[recurring.client_id].first_name,
                        clients[recurring.client_id].last_name,
                        clients[recurring.client_id].organization)
    logging.debug('page %s' % page)
    recurring_response = c.recurring.list(page=page)
#pprint.pprint(client_ids)


