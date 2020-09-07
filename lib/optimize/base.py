from .lineups import ProjectionOptimizerFD
from lib.projections.team_point_percentages import run as run_team_point_percentages
#from lib.projections.scaled_pp36_proj_minutes import run as run_scaled_pp36_proj_minutes
from lib.projections.scaled_med_outside_proj_mins_avg_pp36 import run as run_scaled_med_outside_proj_mins_avg_pp36
import pandas as pd
from lib.export import ExporterFD
from db.db import actor

fd_proj_query = '''
SELECT
        pid,
        player_name,
        team_abbrv,
        fd_positions AS pos,
        fd_salary AS sal,
        fd_points AS pts,
        act_fd_pts AS act_pts,
        fd_id as site_id,
        proj_sub_id,
        proj_minutes,
        act_minutes
FROM
        stat_line_projection_subs_vw
WHERE
        date = %(date)s
        AND source = %(source)s
        AND version = %(version)s
        AND listing_number = %(listing_number)s
        AND user_id = %(user_id)s
'''


def export_lineups(filename, lineups):
    efd = ExporterFD(lineups, filename=filename)
    efd.export()


def doit(site, date, source, version, user_id, filename=None, num_lineups=1):
    if site == 'fd':
        site_id = 2
    lineup_ids = []
    lineups = []
    for _ in range(num_lineups):
        # create and insert, where listing_number and count are returned.
        # only need listing number though
        print(date, source, version, user_id)
        listing_number, _ = run_scaled_med_outside_proj_mins_avg_pp36(date, source, version, user_id)
        # optimize
        print(date, source, version, listing_number, user_id)
        qparams = {'date': date, 'source': source, 'version': version, 'listing_number': listing_number,
                   'user_id': user_id}

        df = pd.read_sql_query(fd_proj_query, actor.conn, params=qparams)
        df = df.fillna(method='ffill')
        lineup = optimize_df(site, date, df)
        lineups.append(lineup)
        lineup_id = ProjectionOptimizerFD.save(lineup, site_id, user_id, date, version, listing_number)
        # append

    print(lineup_ids)
    if filename:
        export_lineups(filename, lineups)



def optimize_df(site, date, projections):
    if site == 'fd':
        optm = ProjectionOptimizerFD(date, projections)
    else:
        pass
    optm.optimize()
    return optm
