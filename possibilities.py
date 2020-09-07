from db.db import actor
import pandas as pd
import numpy as np

import utils

#the standard dev from the projected points to actual points.
PROJ_PTS_STD = 10.303283


def normal_dist_random(proj_pts):
    return np.random.normal(proj_pts, PROJ_PTS_STD)


def _generate_percentages(slidf):
    """ For the projetions, we want to take a random sample of points,
        and then scale that to get percentages for the players.
    """
    rand_projections = []
    for projection in projections:
        rand_points = normal_dist_random(guess, STD)
        rand_projections.append(rand_points)
    pass
    sum_raw = sum(rand_projections)
    norm = [float(i)/sum_raw for i in rand_projections]


SLI_QUERY = 'select name, minutes, fd_salary, fd_points, fd_proj_points from stat_line_infos where date=%s and team_abbrv=%s and proj_version=%s and sl_active and minutes > 0'

def create_team_points(team_fantasy_points, date, team_abbrv, proj_version='0.2-lin-reg-dfn-min'):
    """ With the projected `team_fantasy_points` for a team, we find the projections
        for the team for that game, and come up with point percentages for the players.
        For example, we take the point distributions, normal guess, and then 
        Goal of this is to make sure that we don't say that every player
        on a team can play great, but that if the team scores `fantasy_points` points,
        what percentage is scored by each player.
    """
    #find the projections for players on that team for that game
    
    slidf = pd.read_sql_query(SLI_QUERY, actor.conn, params=(date, team_abbrv, proj_version,))
    print(slidf['fd_proj_points'].sum())
    slidf['normalized_fd_pts'] = normal_dist_random(slidf['fd_proj_points'])
    print(slidf)


if __name__ == '__main__':
    create_team_points(255, '2020-01-08', 'MIL', proj_version='0.1-dfn')
    pass