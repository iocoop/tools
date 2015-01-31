#!/usr/bin/env python

# Dependencies
# pycrypto gspread oauth2client

# Deployed location :
# srv1.msp.iocoop.org:/var/www/iocoop.org/django-iocoop/tools/
# Key location
# srv1.msp.iocoop.org:/etc/IO Cooperative Inventory-ce754dcd775f.pem
# srv1.msp.iocoop.org:/etc/IO Cooperative Inventory-ce754dcd775f.p12

from oauth2client.client import SignedJwtAssertionCredentials
import gspread
from django.conf import settings


WORKSHEETS = ['SCL-001.M03.01', 'SCL-001.M03.02', 'SCL-001.M03.03', 'MSP']


def authorize(email, keyfile, scope, secret=None):
  '''
  Authenticate to Google Drive and return an authorization.
  '''
  try:
    with open(keyfile) as keyfile_object:
      private_key = keyfile_object.read()
    if secret:
      credentials = SignedJwtAssertionCredentials(email, private_key, scope, secret)
    else:
      credentials = SignedJwtAssertionCredentials(email, private_key, scope)
    return gspread.authorize(credentials)
  except Exception as ex:
    return None

 
def get_client_systems(freshbooks_id):
  '''
  Return a list of systems belonging to specified freshbooks_id (int).
  '''
  scope = ['https://spreadsheets.google.com/feeds']
  client = authorize(settings.GSPREAD_EMAIL, settings.GSPREAD_PEM, scope)
  if client:
    spreadsheet = client.open('IO Cooperative Colo Inventory')
    systems = []
    for sheet in WORKSHEETS:
      worksheet = spreadsheet.worksheet(sheet)
      records = worksheet.get_all_records()
      for record in records:
        if record['Freshbooks Client ID']  == freshbooks_id:
          record['rack'] = sheet
          systems.append(record)
    return systems
