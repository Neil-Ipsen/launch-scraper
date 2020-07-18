import requests
from bs4 import BeautifulSoup

URL = 'https://spaceflightnow.com/launch-schedule/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')