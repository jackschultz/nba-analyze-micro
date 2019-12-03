import json
import calendar
import datetime
from collections import defaultdict
import requests

from export import export_lineups

local_optimize_url = 'http://127.0.0.1:5000/optimize'

site = 'fd'
site_id = 2 # that's the id in the db.


actuals_points = []
projection_points = []


def ping_optimizer(date, site='fd', version=None, excludes=[], includes=[]):
    response = requests.get(local_optimize_url, data={'date': date, 'site': site, 'exclude': excludes, 'includes': includes, 'version': version})
    resj = response.json()
    lineup = defaultdict(list)
    for player in resj['players']:
        pos = player['pos']
        pid = player[f'{site}_id']
        lineup[pos].append(pid)
    actual_points = resj['actuals']['points']
    projected_points = resj['projections']['points']
    print(f"Projected Points: {resj['projections']['points']}")
    print(f"Actual Points: {actual_points}")
    actuals_points.append(actual_points)
    projection_points.append(projected_points)

    players = resj['players']
    for p in players:
        print(p['sal'], p['name'])
    player_ids = [p['pid'] for p in players]
    #for player in players:
    #   print(player['name'])
    return player_ids, lineup


def create_lineups(date, site, version, levels=3, excludes=[], includes=[]):
    total_excludes = []
    lineups = []
    excludes = [0,10000000]
    for i in range(1,2):
        player_ids, lineup = ping_optimizer(date, version=version, excludes=excludes, includes=includes)
        lineups.append(lineup)
        for pid in player_ids:
            excludes = [0]
            excludes.append(pid)
            total_excludes.append(pid)
            #ping_optimizer(date, excludes=excludes)

    for i in range(levels):
        print(f'Removing all of the top top players. Round {i}.')
        player_ids, lineup = ping_optimizer(date, version=version, excludes=total_excludes, includes=includes)
        lineups.append(lineup)
        for pid in player_ids:
            total_excludes.append(pid)
            #ping_optimizer(date, excludes=total_excludes)

    print(f'Projected Points')
    print(sorted(projection_points))

    if not None in actuals_points:
        print(f'Actual Points')
        print(sorted(actuals_points))

    return lineups

if __name__ == '__main__':
    date = '2019-11-27'
    version = '0.2-lin-reg-dfn-min'
    #version = '0.1-dfn'
    site = 'fd'
    lineups = create_lineups(date, site, version)
    filename = f"{date}-{version.replace('.', '-')}.csv"
    export_lineups(lineups, filename=filename)
