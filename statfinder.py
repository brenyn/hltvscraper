#!/usr/bin/env python

#########################################################################################
# Written by: Brenyn Kissoondath
# Date: May 14, 2020
# Purpose: Prototype that navigates from match page to 2 teams stat pages
# Input(s): URL to match
# Output(s): URLs to team stats
#
# Notes to self:
# 1. A less janky way of doing this would be to find team identifier from team page URL
# and use that + team name to navigate to matches tab
#
# 2. Only grab stats for past 3 months (complete step 1 first)
#########################################################################################

import requests
from bs4 import BeautifulSoup

testMatchURL = "https://www.hltv.org/matches/2341368/swedish-canadians-vs-infinity-esea-mdl-season-34-north-america"

def statfinder (matchURL):
	response = requests.get(matchURL)
	
	matchPageSoup = BeautifulSoup(response.content, 'html.parser')
	
	team1Soup = matchPageSoup.find("div",class_="team1-gradient")
	team2Soup = matchPageSoup.find("div",class_="team2-gradient")
	
	team1URL = "https://hltv.org" + team1Soup.find("a").get('href') + "#tab-statsBox"
	team2URL = "https://hltv.org" + team2Soup.find("a").get('href') + "#tab-statsBox"
	
	
	# BELOW THIS LINE IS TOO JANKY, PROBABLY WILL BREAK IN FUTURE, ONLY USING FOR PROTOTYPE
	# CHANGE ACCORDING TO TODO IN FINAL VERSION
	
	
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