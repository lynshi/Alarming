from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def queryCal():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(calendarId='jqkes0nih4tu0m0cjcdjg5qs30@group.calendar.google.com', timeMin=now, maxResults=1).execute()
    events = eventsResult.get('items', [])
    checkEvents(events)

def checkEvents(events):
    if not events:
        print('No upcoming events found.')
        return;
    
    for firstEvent in events:
        event = firstEvent['start'].get('dateTime')
        print(event)
        """this is awful coding practice"""
        eventYear = event[0]+event[1]+event[2]+event[3]
        if event[5] != '0':
            eventMonth = event[5] + event[6]
        else:
            eventMonth = event[6]
        if event[8] != '0':
            eventDay = event[8] + event[9]
        else:
            eventDay = event[9]
        if event[11] != '0':
            eventHour = event[11] + event[12]
        else:
            eventHour = event[12]
        if event[14] != '0':
            eventMinute = event[14] + event[15]
        else:
            eventMinute = event[15]
        timeNow = datetime.datetime.now()
        print(timeNow)
        
        """check for events within the next 24 hours"""
        if eventYear == str(timeNow.year) and eventMonth == str(timeNow.month):
            print('same month/year!')
            if eventDay == str(timeNow.day):
                print('same day')
            elif eventDay == str(timeNow.day+1):
                if int(eventHour) <= timeNow.hour:
                    print('within range')
                else:
                    return;
            else:
                return;
        else:
            return

def main():
    while(1):
        timeNow = datetime.datetime.now()
        if 1:
            print('stopped')
            queryCal()
            return
        # if timeNow.minute == 6:
        #     print('stopped')
        #     queryCal()
        #     return


if __name__ == '__main__':
    main()
