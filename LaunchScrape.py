import requests
from bs4 import BeautifulSoup
from apiclient.discovery import build
from httplib2 import Http 
from oauth2client import file, client, tools
import pytz
from datetime import datetime, timedelta

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
        if flags else tools.run(flow, store)
CAL = build('calendar', 'v3', http=creds.authorize(Http()))

def is_dst(zonename):
    tz = pytz.timezone(zonename)
    now = pytz.utc.localize(datetime.utc_now())
    return now.astimezone(tz).dst() != timedelta(0)

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
        splitAdd = date.text + "\n" + mission.text + "\n" + window.text + "\n" + description.text + "\n"
        split.append(splitAdd)

    missionDate = split[0]
    missionTitle = split[1]
    missionWindow = split[2]
    missionDescription = split[3]

    if is_dst("America/New_York"):
        GMT_OFF = '-04:00'
    else:
        GMT_OFF = '-05:00'
    
    for i in split:
        EVENT = {
            'summary': split[3],
            'start':   {'dateTime': split[0] % GMT_OFF},
            'end':     {'dateTime': split[0] % GMT_OFF}
        }
    
        e = CAL.events().insert(calendarId='primary', sendNotifications=True, body=EVENT).execute()
    
    return

siteParse()