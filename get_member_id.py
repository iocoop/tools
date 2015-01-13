#!/usr/bin/env python

from refreshbooks import api
import ConfigParser
import argparse
import pprint
import logging

logging.basicConfig(level=logging.INFO)

parser = argparse.ArgumentParser(description='Determine a freshbooks client_id from a client email address')
parser.add_argument('email_address', nargs='*',
                   help='email address to search for')
parser.add_argument('--config', '-c', dest='config', default='/etc/freshbooks.cfg',
                   help='config file name (default: /etc/freshbooks.cfg)')

args = parser.parse_args()

config = ConfigParser.RawConfigParser()
config.read(args.config)

api_token = config.get('Freshbooks', 'api_token')

c = api.TokenClient(
    'iocoop.freshbooks.com',
    api_token,
    user_agent='get_member_id.py/1.0'
)

client_ids = {}
for email_address in args.email_address:
    client_ids[email_address] = {}
    
client_response = c.client.list()
logging.debug('total pages : %s' % client_response.clients.attrib['pages'])
for page in range(2, int(client_response.clients.attrib['pages']) + 2):
    for client in client_response.clients.client:
        logging.debug('client.email = %s' % client.email)
        if len(client_ids) > 0:
            for email_address in args.email_address:
                if str(client.email).lower() == email_address.lower():
                    client_ids[email_address][client.first_name + ' ' + client.last_name + ' : ' + client.organization] = client.client_id
        else:
            # logging.info("%s '%s' '%s %s'" % (str(client.email).lower(), client.organization, client.first_name, client.last_name))
            #logging.info(str(client.email).lower())
            print '"%s", "%s %s", "%s"' % (str(client.email).lower(), client.first_name, client.last_name, client.organization)

    logging.debug('page %s' % page)
    client_response = c.client.list(page=page)
pprint.pprint(client_ids)
