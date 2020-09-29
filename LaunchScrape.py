from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#SCOPES = ['https://www.googleapis.com/auth/calendar']
#creds = None
# if os.path.exists('token.pickle'):
#    with open('token.pickle', 'rb') as token:
#        creds = pickle.load(token)
# if not creds or not creds.valid:
#    if creds and creds.expired and creds.refresh_token:
#        creds.refresh(Request())
#    else:
#        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#        creds = flow.run_local_server(port=0)
#    with open('token.pickle', 'wb') as token:
#        pickle.dump(creds, token)
#
#service = build('calendar', 'v3', credentials=creds)


def siteParse():
    # Fetch source URL
    URL = 'https://spaceflightnow.com/launch-schedule/'
    page = requests.get(URL)

    # Initialize Beautiful Soup and results object
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id="main-content")

    # Initialize main body objects
    missionHead = results.find_all('div', class_='datename')
    missionData = results.find_all('div', class_='missiondata')
    missionBody = results.find_all('div', class_='missdescrip')

    # Instantiate arrays for missionData and missionBody to avoid for loop nesting issues.
    data = []
    for i in missionData:
        data.append(i)

    body = []
    for i in missionBody:
        body.append(i)

    split = []

    # Group and print mission details.
    x = -1
    for missionHead in missionHead:
        x = x + 1
        date = missionHead.find('span', class_='launchdate')
        mission = missionHead.find('span', class_='mission')
        window = data[x]
        description = body[x]

        split.append(date.text)
        split.append(mission.text)
        split.append(window.text)
        split.append(description.text)

    missionDate = split[0]
    missionTitle = split[1]
    missionWindow = split[2]
    missionDescription = split[3]

    # for i in split:
    #   event = {
    #        'summary':     split[1],
    #        'description': split[3],
    #        'start':       {
    #            'dateTime': split[0],
    #            'timeZone': 'America/New_York'
    #        },
    #        'end':         {
    #            'dateTime': split[0],
    #            'timeZone': 'America/New_York'
    #        },
    #        'reminders':   {
    #            'useDefault': False,
    #            'overrides': [{
    #                'method': 'popup',
    #                'minutes': 48*60
    #            },
    #            {
    #            'method': 'popup',
    #            'minutes': 3*60
    #            },],
    #        },
    #    }
    #
    #    event = service.events().insert(calendarId='primary', sendNotifications=True, body=event).execute()
    #
    print(split[3])

    return


siteParse()
