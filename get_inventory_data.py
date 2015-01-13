#!/usr/bin/env python

# Dependencies
# pycrypto gspread oauth2client

# Deployed location :
# srv1.msp.iocoop.org:/var/www/iocoop.org/django-iocoop/tools/
# Key location
# srv1.msp.iocoop.org:/etc/IO Cooperative Inventory-ce754dcd775f.pem
# srv1.msp.iocoop.org:/etc/IO Cooperative Inventory-ce754dcd775f.p12

import gspread
from oauth2client.client import SignedJwtAssertionCredentials

def find_column(column_name, column_names):
	return (column_names.index(column_name) 
		if column_name in column_names 
		else False)

client_email = '888367538254-l1imqqmhjnmrjuc4ns7at0q0i2nkka66@developer.gserviceaccount.com'

# pycrypto uses .pem format instead of .p12 like python-openssl does
# http://stackoverflow.com/questions/27305867/google-api-access-using-service-account-oauth2client-client-cryptounavailableerr
with open("/etc/IO Cooperative Inventory-ce754dcd775f.pem") as f:
  private_key = f.read()
scope = ['https://spreadsheets.google.com/feeds']

credentials = SignedJwtAssertionCredentials(client_email, 
                                            private_key,
                                            scope)
                                            # Fourth parameter can be private_key_password if it's not the defaulf of 'notasecret'
                                            # https://google-api-python-client.googlecode.com/hg/docs/epy/oauth2client.client.SignedJwtAssertionCredentials-class.html
gc = gspread.authorize(credentials)
sh = gc.open("IO Cooperative Colo Inventory")
worksheet_list = sh.worksheets()
for worksheet in worksheet_list:
	# worksheet = sh.worksheet("SCL-001.M03.01")
	list_of_lists = worksheet.get_all_values()
	column_number = find_column('Freshbooks Client ID', list_of_lists[0])