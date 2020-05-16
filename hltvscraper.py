#!/usr/bin/env python

#########################################################################################
# Written by: Brenyn Kissoondath
# Date: May 14, 2020
# Purpose: Complete prototype combining urlscraper, statfinder, and tablescraper
# Input(s): HLTV website URL
# Output(s): Game stats to excel/google sheets/csv (TBD)
#
# Notes to self:
# 
# Exiting with error(seems to be scraping correctly except for last game):
# Traceback (most recent call last):
#  File "<stdin>", line 2, in <module>
#  File "<stdin>", line 21, in statfinder
# AttributeError: 'NoneType' object has no attribute 'get'
#
# Last game second team hasnt been decided yet, probably the cause of error.
# Look into error handling or ignore games that don't have teams decided
# Not a big deal right now but will be in the future for large tournament brackets
#########################################################################################

import requests
from bs4 import BeautifulSoup
from datetime import date
import csv

listofkeys = ['date','event','opponent','mapPlayed','result']
filename = "matchday-"+ str(date.today()) + ".csv"

with open (filename,'w') as csvfile:
	
	csv_writer = csv.DictWriter(csvfile,fieldnames = listofkeys, delimiter=',')
	
	csv_writer.writeheader()

def statfinder (matchURL):
	startDate = '2020-02-16'
	endDate = str(date.today())
	timeFilter = '?startDate=' + startDate + '&endDate=' + endDate
	response = requests.get(matchURL)
	
	matchPageSoup = BeautifulSoup(response.content, 'html.parser')
	
	team1Soup = matchPageSoup.find("div",class_="team1-gradient")
	team2Soup = matchPageSoup.find("div",class_="team2-gradient")
	
	team1Name = team1Soup.find("div",class_="teamName").text.strip()
	team2Name = team2Soup.find("div",class_="teamName").text.strip()
	
	team1ID = team1Soup.find("img",class_="logo").get('src')
	team1ID = ''.join(filter(str.isdigit,team1ID))
	team2ID = team2Soup.find("img",class_="logo").get('src')
	team2ID = ''.join(filter(str.isdigit,team2ID))
	
	team1URL = team1Soup.find("a").get('href')
	team2URL = team2Soup.find("a").get('href')
	
	team1URL = 'https://www.hltv.org/stats/teams/matches/' + team1ID + '/' + team1Name + timeFilter
	team2URL = 'https://www.hltv.org/stats/teams/matches/' + team2ID + '/' + team2Name + timeFilter
	
	return (team1URL, team2URL)

def tablescraper (statURLs):
	gamestats = dict.fromkeys(listofkeys,None)
	
	for url in statURLs:
		r = requests.get(url)
		
		soup = BeautifulSoup(r.text, 'html.parser')
		
		# only interested in results table, save results to tablesoup variable
		tablesoup = soup.tbody
		
		# find all tr elements, each element is a unique game.
		# note: not using css selectors because there are 2 different tr elements used for some reason.
		# group-2 first and group-1 first. Seems more efficient to just find all tr elements.
		gameTable = tablesoup.find_all('tr') 
		
		with open (filename,'a') as csvfile:
			
			csv_writer = csv.DictWriter(csvfile,fieldnames = listofkeys, delimiter=',')
			
			for game in gameTable:
				cells = game.find_all('td')
				gamestats['date'] = (cells[0].text.strip())
				gamestats['event'] = (cells[1].text.strip())
				gamestats['opponent'] = (cells[3].text.strip())
				gamestats['mapPlayed'] = (cells[4].text.strip())
				gamestats['result'] = (cells[5].text.strip())
				csv_writer.writerow(gamestats)


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

statURLs = []
for matchURL in gameDayURLs:
	tablescraper(statfinder(matchURL))
