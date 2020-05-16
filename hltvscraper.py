#!/usr/bin/env python

#########################################################################################
# Written by: Brenyn Kissoondath
# Date: May 14, 2020
# Purpose: Complete prototype combining urlscraper, statfinder, and tablescraper
# Input(s): HLTV website URL
# Output(s): Game stats to excel/google sheets/csv (TBD)
#########################################################################################

import requests
from bs4 import BeautifulSoup

def statfinder (matchURL):
	response = requests.get(matchURL)
	
	matchPageSoup = BeautifulSoup(response.content, 'html.parser')
	
	team1Soup = matchPageSoup.find("div",class_="team1-gradient")
	team2Soup = matchPageSoup.find("div",class_="team2-gradient")
	
	team1URL = "https://hltv.org" + team1Soup.find("a").get('href') + "#tab-statsBox"
	team2URL = "https://hltv.org" + team2Soup.find("a").get('href') + "#tab-statsBox"
	
	#Finding stats for team 1
	response = requests.get(team1URL)
	
	team1Soup = BeautifulSoup(response.content, 'html.parser')
	team1Name = team1Soup.find("div",class_="profile-team-name text-ellipsis").text.strip()
	
	team1Soup = team1Soup.find("div", {"id": "statsBox"})
	team1URL = "https://hltv.org" + team1Soup.find_all("a",class_="moreButton")[-1].get('href')
	
	response = requests.get(team1URL)
	
	team1Soup = BeautifulSoup(response.content, 'html.parser')
	
	team1Soup = team1Soup.find("div",class_="tabs standard-box")
	team1URL = "https://hltv.org" + team1Soup.find_all("a",class_="stats-top-menu-item stats-top-menu-item-link")[0].get('href')
	
	#Finding stats for team 2
	response = requests.get(team2URL)
	
	team2Soup = BeautifulSoup(response.content, 'html.parser')
	team2Name = team2Soup.find("div",class_="profile-team-name text-ellipsis").text.strip()
	
	team2Soup = team2Soup.find("div", {"id": "statsBox"})
	team2URL = "https://hltv.org" + team2Soup.find_all("a",class_="moreButton")[-1].get('href')
	
	response = requests.get(team2URL)
	
	team2Soup = BeautifulSoup(response.content, 'html.parser')
	
	team2Soup = team2Soup.find("div",class_="tabs standard-box")
	team2URL = "https://hltv.org" + team2Soup.find_all("a",class_="stats-top-menu-item stats-top-menu-item-link")[0].get('href')
	
	return (team1URL, team2URL)

def tablescraper (teamstats):
	for url in teamstats:
		gamecount = 0
		
		games = []
		listofkeys = ['date','event','opponent','mapPlayed','result']
		
		r = requests.get(url)
		
		soup = BeautifulSoup(r.text, 'html.parser')
		
		# only interested in results table, save results to tablesoup variable
		tablesoup = soup.tbody
		
		# find all tr elements, each element is a unique game.
		# note: not using css selectors because there are 2 different tr elements used for some reason.
		# group-2 first and group-1 first. Seems more efficient to just find all tr elements.
		gameTable = tablesoup.find_all('tr')
		
		for game in gameTable:
			games.append(dict.fromkeys(listofkeys,None))
			cells = game.find_all('td')
			games[gamecount]['date'] = (cells[0].text.strip())
			games[gamecount]['event'] = (cells[1].text.strip())
			games[gamecount]['opponent'] = (cells[3].text.strip())
			games[gamecount]['mapPlayed'] = (cells[4].text.strip())
			games[gamecount]['result'] = (cells[5].text.strip())
			gamecount+=1
		
		print (games)#print games for test, need to export to csv/excel/google sheets here


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

for matchURL in gameDayURLs:
	tablescraper(statfinder(matchURL))
