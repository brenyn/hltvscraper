#!/usr/bin/env python

#########################################################################################
# Written by: Brenyn Kissoondath
# Date: May 14, 2020
# Purpose: Prototype that parses a team's stat table and stores in a data structure
# Input(s): Team's stat page
# Output(s): TBD
#
# Notes to self:
# 1. Add home team name to list of keys for sorting purposes
#########################################################################################

import requests
from bs4 import BeautifulSoup

def tablescraper (url):
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

	return games