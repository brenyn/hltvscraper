#!/usr/bin/env python

#########################################################################################
# Written by: Brenyn Kissoondath
# Date: May 14, 2020
# Purpose: Prototype that navigates from match page to 2 teams stat pages
# Input(s): URL to match
# Output(s): URLs to team stats
#
# Note to self: breaking for teams with numbers in name
#########################################################################################

import requests
from bs4 import BeautifulSoup
from datetime import date

testMatchURL = "https://www.hltv.org/matches/2341368/swedish-canadians-vs-infinity-esea-mdl-season-34-north-america"

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