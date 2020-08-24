import requests
from bs4 import BeautifulSoup

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

    # Group and print mission details.
    x = -1
    for missionHead in missionHead:
        x = x + 1
        date = missionHead.find('span', class_='launchdate')
        mission = missionHead.find('span', class_='mission')
        window = data[x]
        description = body[x]
        return(date.text + "\n" + mission.text + "\n" + window.text + "\n" + description.text)