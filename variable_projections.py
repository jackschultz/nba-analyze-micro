import pandas as pd

from db.db import actor
from scores import create_possible_score

gq = "select * from pre_game_infos where date=%s"

sliq = "select * from stat_line_infos where proj_version=%s and date=%s;"

if __name__ == '__main__':
    proj_version = '0.2-lin-reg-dfn-min'
    proj_version = '0.1-dfn'
    date = '2019-12-03'
    #games = actor.find_games_by_date(date)
    games = actor.call_custom_all(gq, (date,))
    sldf = pd.read_sql_query(sliq, actor.conn, params=(proj_version, date,))# actor.call_custom_all(sliq, )
    print(sldf)
    for game in games:
        htm_abbrv = game['hmt_abbrv']
        awt_abbrv = game['awt_abbrv']
        odds = float(game['odds'])
        over_under = float(game['over_under'])
        print(odds, over_under)
        print(awt_abbrv, htm_abbrv)
        ats, hts = create_possible_score(odds, over_under)
        print(ats, hts)
        #import pdb;pdb.set_trace()

        asdf = sldf.query("team_abbrv == '%s'" % htm_abbrv)
        print(asdf["proj_minutes"].sum())
