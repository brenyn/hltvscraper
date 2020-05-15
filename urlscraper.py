#!/usr/bin/env python

#########################################################################################
# Written by: Brenyn Kissoondath
# Date: May 14, 2020
# Purpose: Prototype that retrieves match URLs from HLTV home page
# Input(s): HLTV URL
# Output(s): URLs to upcoming matches
#
# Notes to self:
# 1. Doesn't parse all matches for long match days (stops at 29 games)
# 2. Also parsing first 2 match days, excluding last game of second match day, when it
# should only be retreiving URLs for the first match day.
# 3. Maybe try different HTML parsers?
#########################################################################################

import requests
from bs4 import BeautifulSoup

gameDayURLs = []

hltvURL = "https://www.hltv.org/matches"

response = requests.get(hltvURL) 

frontPageSoup = BeautifulSoup(response.content, 'html.parser')

upcomingMatches = frontPageSoup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['match-day'])

gameDayURLs = upcomingMatches[0].find_all("a",class_="a-reset")

urlCounter = 0

for url in gameDayURLs:
	url = gameDayURLs[urlCounter].get('href')
	gameDayURLs[urlCounter] = "https://hltv.org" + url
	urlCounter += 1


#tags = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['message'])

#upcomingMatches = frontPageSoup.find("div",class_="match-day")
#soup.find_all("div", class_="stylelistrow")