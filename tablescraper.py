#!/usr/bin/env python

#########################################################################################
# Written by: Brenyn Kissoondath
# Date: May 14, 2020
# Purpose: Prototype that parses a team's stat table and stores in a data structure
# Input(s): Team's stat page
# Output(s): TBD
#
# Notes to self:
# 1. Implement way of retreiving games vs different team rankings. meaning 6 different
# game data structs, one for each ranking filter on HLTV, check structs against each
# other to eliminate duplicates.
#
# 2. Alternatively could find each team's HLTV ranking from team page and use that to sort
# the teams. I like this idea better actually. Do this instead. Would make it much easier
# to sort data later and is less janky/subject to break if they update the site.
#########################################################################################

import requests
from bs4 import BeautifulSoup



testurl = "https://hltv.org/stats/teams/matches/9963/Infinity"

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



































#	for cell in cells:
#		if "time" in cell:
#			print(cell)


#print((game.select("td.time")).getText())
#games[gamecount]['date'] = (cells[0])
#games[gamecount]['date'] = (unstrippedTime[0]).text

#Initial data structure concept################
#games = [
#		{
#			'date':'11/05/20',
#			'event':'Loot Bet',
#			'event2':'Loot Bet',
#			'opponent':'Gambit Youngsters',
#			'mapPlayed':'Dust2',
#			'result':'8 - 16'
#		}]
##############################################

#    for cell in cells:
#        print(cell.getText())	#print values found in td cells