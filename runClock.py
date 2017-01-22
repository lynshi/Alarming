from __future__ import print_function
import httplib2
import os
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import serial
import time

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

alarmOffset = []
alarmOffset.append(0)
alarmOffset.append(0)


def get_credentials(): #######################################################################################################################     DO NOT EDIT
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

def queryCal(): #######################################################################################################################     DO NOT EDIT
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    eventsResult = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    return checkEvents(events)

def checkEvents(events):
    if not events:
        print('No upcoming events found.')
        return ['-1', '-1', '-1', '-1', '-1', '-1'];
    
    for thisEvent in events:
        event = thisEvent['start'].get('dateTime')
        print(event + thisEvent['summary'])

        #splits API datetime data into chunks that can be compared with Python datetime
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

        #current time    
        timeNow = datetime.datetime.now()
        print(timeNow)

        #Case one: The alarm for this event should occur on the same day at a later time, most likely possibility
        if int(eventMonth) == timeNow.month and int(eventDay) == timeNow.Day and int(eventYear) == timeNow.year and int(eventHour) - alarmOffset[0] >= timeNow.hour and int(eventMinute) - alarmOffset[1] > timeNow.minute:
            return [eventMonth, eventDay, eventYear, str(int(eventHour) - alarmOffset[0]), str(int(eventMinute) - alarmOffset[1]), thisEvent['summary']]

        #Case two: The alarm for this event should occur in a future year
        if int(eventYear) > timeNow.year:
            return [eventMonth, eventDay, eventYear, str(int(eventHour) - alarmOffset[0]), str(int(eventMinute) - alarmOffset[1]), thisEvent['summary']]

        #Case three: The alarm for this event should occur in a future month in this year (future years have been eliminated)
        if int(eventMonth) > timeNow.month:
            return [eventMonth, eventDay, eventYear, str(int(eventHour) - alarmOffset[0]), str(int(eventMinute) - alarmOffset[1]), thisEvent['summary']]

        #Case four: The alarm for this event should occur on a later day in this month (future months and years have been eliminated)
        if int(eventDay) > timeNow.Day:
            return [eventMonth, eventDay, eventYear, str(int(eventHour) - alarmOffset[0]), str(int(eventMinute) - alarmOffset[1]), thisEvent['summary']]
    
    #If an impossibly bad schedule with 10 overlapping events happening at the current time is encountered, give up and wait until one event is finished
    return ['-1', '-1', '-1', '-1', '-1', '-1'];

def main():
    alarmTime = []
    for i in range(0, 6): #[month, day, year, hour, minute, event name]
        alarmTime.append('-1')

    port = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=5.0) #enable serial communication with Arduino

    while(1):
        print('Finding next event')
        #finds next event to set an alarm for
        alarmTime = queryCal()

        timeNow = datetime.datetime.now() #gets the current time
        message = "" #message to send to Arduino

        #format for sending date and time data to the clock; adds leading 0's because they are not included automatically
        if len(str(timeNow.month)) == 1:
            message = message + "0" + str(timeNow.month)
        else:
            message = message + str(timeNow.month)
        if len(str(timeNow.day)) == 1:
            message = message + "0" + str(timeNow.day)
        else:
            message = message + str(timeNow.day)
        if len(str(timeNow.year)) == 1:
            message = message + "0" + str(timeNow.year)
        else:
            message = message + str(timeNow.year)
        if len(str(timeNow.hour)) == 1:
            message = message + "0" + str(timeNow.hour)
        else:
            message = message + str(timeNow.hour)

        if len(str(timeNow.minute)) == 1:
            message = message + "0" + str(timeNow.minute)
        else:
            message = message + str(timeNow.minute)

        if alarmTime[0] == str(timeNow.month) and alarmTime[1] == str(timeNow.day) and alarmTime[2] == str(timeNow.year) and alarmTime[3] == str(timeNow.hour) and alarmTime[4] == str(timeNow.minute):
            print('ALARM!!!')
            message = message + "1" + alarmTime[5] + '\n'

            #reset alarm values
            for i in range(0, 6):
                alarmTime[i] = '-1'

            print(message)
            port.write(message) #send message to Arduino
            #Arduino needs to pause alarm message updating here
        else:
            message = message + "0" + '\n'
            print(message)
            port.write(message) #send message to Arduino
        
        time.sleep(1)


if __name__ == '__main__':
    main()