#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 23:16:16 2022

@author: christian
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import regex

nets_url = (f'https://www.basketball-reference.com/teams/BRK/2023.html')

nets_res = requests.get(nets_url)

nets_soup = BeautifulSoup(nets_res.content, 'lxml')

nets_per_game = nets_soup.find(name = 'table', attrs ={'id' : 'per_game'})

nets_stats = []

for row in nets_per_game.find_all('tr')[1:]:  

    player = {}
    player['Name'] = row.find('a').text.strip()
    player['Age'] = row.find('td', {'data-stat' : 'age'}).text
    player['Min PG'] = row.find('td', {'data-stat' : 'mp_per_g'}).text
    player['Field Goal %'] = row.find('td', {'data-stat' : 'fg_pct'}).text
    player['Rebounds PG'] = row.find('td', {'data-stat' : 'trb_per_g'}).text
    player['Assists PG'] = row.find('td', {'data-stat' : 'ast_per_g'}).text
    player['Steals PG'] = row.find('td', {'data-stat' : 'stl_per_g'}).text
    player['Blocks PG'] = row.find('td', {'data-stat' : 'blk_per_g'}).text
    player['Turnovers PG'] = row.find('td', {'data-stat' : 'tov_per_g'}).text
    player['Points PG'] = row.find('td', {'data-stat' : 'pts_per_g'}).text
    nets_stats.append(player)

pd.DataFrame(nets_stats)

# Making a list of dictionaries to then convert into a pd.DataFrame
nets_info = []
for row in nets_per_game.find_all('tr')[1:]:  # Excluding the first 'tr', since that's the table's title head

    player = {}
    player['Name'] = row.find('a').text.strip()
    player['Age'] = row.find('td', {'data-stat' : 'age'}).text
    player['Min PG'] = row.find('td', {'data-stat' : 'mp_per_g'}).text
    player['Field Goal %'] = row.find('td', {'data-stat' : 'fg_pct'}).text
    player['Rebounds PG'] = row.find('td', {'data-stat' : 'trb_per_g'}).text
    player['Assists PG'] = row.find('td', {'data-stat' : 'ast_per_g'}).text
    player['Steals PG'] = row.find('td', {'data-stat' : 'stl_per_g'}).text
    player['Blocks PG'] = row.find('td', {'data-stat' : 'blk_per_g'}).text
    player['Turnovers PG'] = row.find('td', {'data-stat' : 'tov_per_g'}).text
    player['Points PG'] = row.find('td', {'data-stat' : 'pts_per_g'}).text

    player_url = ('https://www.basketball-reference.com/' + row.find('a').attrs['href'])
    player_rest = requests.get(player_url)
    player_soup = BeautifulSoup(player_rest.content, 'lxml')
    player_info = player_soup.find(name = 'div', attrs = {'itemtype' : 'https://schema.org/Person'})

    count = 1
    player_links= []
    for link in player_info.find_all('a'):
        player_links.append(link.get('href'))

    if 'twitter' in player_links[1]:
        player['Twitter Handle'] = player_links[1].replace('https://twitter.com/', '')
    else:
        player['Twitter Handle'] = 'Not Listed'

    s = str(player_info.find_all('p'))

    weight = regex.search('\"weight\">(.*)lb</span>', s)
    position = regex.search('Position:\n  </strong>\n (.*)\n\n', s)
    height = regex.search('\"height\">(.*)</span>,\xa0<span itemprop="weight', s)
    player['Height'] = height.group(1).strip()
    player['Weight (Lbs)'] = weight.group(1).strip()
    player['Position'] = position.group(1).strip()

    nets_info.append(player)
        
pd.DataFrame(nets_info)