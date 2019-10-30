import json
import calendar
import datetime

import requests

local_optimize_url = 'http://127.0.0.1:5000/optimize'
date = '2019-10-25'
date = '2019-01-20'

site = 'fd'
site_id = 2 # that's the id in the db.

from db.finders import get_contests_on_date_for_site

actuals_points = []


def ping_optimizer(date, site='fd', version='0.1-avg-5', excludes=[]):
    response = requests.get(local_optimize_url, data={'date': date, 'site': site, 'exclude': excludes, 'version': version})
    print(response.url)
    print(response.request.url)
    print(response.request.body)
    resj = response.json()
    actual_points = resj['actuals']['points']
    print(f"Projected Points: {resj['projections']['points']}")
    print(f"Actual Points: {actual_points}")
    actuals_points.append(actual_points)

    players = resj['players']
    player_ids = [p['pid'] for p in players]
    #for player in players:
    #   print(player['name'])
    return player_ids

'''
year = 2019
month = 1
num_days = calendar.monthrange(year, month)[1]
days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
excludes = []
for day in days:
    date = day.isoformat()
    ping_optimizer(date, excludes=excludes)
'''

total_excludes = []
excludes = [0,10000000]
for i in range(1,2):
    player_ids = ping_optimizer(date, excludes=excludes)
    for pid in player_ids:
        excludes = [0]
        excludes.append(pid)
        total_excludes.append(pid)
        ping_optimizer(date, excludes=excludes)


print(total_excludes)
print(f'Removing all of the top top players. Round two.')
for i in range(1,2):
    player_ids = ping_optimizer(date, excludes=total_excludes)
    for pid in player_ids:
        total_excludes.append(pid)
        ping_optimizer(date, excludes=total_excludes)

print(total_excludes)

print(f'Removing all of the top top players. Round three.')
for i in range(1,2):
    player_ids = ping_optimizer(date, excludes=total_excludes)
    for pid in player_ids:
        total_excludes.append(pid)
        ping_optimizer(date, excludes=total_excludes)


print(sorted(actuals_points))


#contests = get_contests_on_date_for_site(date, site_id)
#print(contests)

