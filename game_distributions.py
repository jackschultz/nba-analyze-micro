import pandas as pd
from db.db import actor
import matplotlib.pyplot as plt
import numpy as np

g1q = '''
SELECT
	*
FROM (
	SELECT
		score - over_under AS diff
	FROM (
		SELECT
			home_team_score + away_team_score AS score,
			over_under
		FROM
			games
		WHERE
			"date" < '2019-05-01'
			AND "date" > '2018-11-01') x) y
WHERE
	diff < 60;
'''

g2q = '''

SELECT
	*
FROM (
	SELECT
		hts - ats AS diff
	FROM (
		SELECT
			home_team_score + odds AS hts,
			away_team_score as ats,
			over_under
		FROM
			games
		WHERE
			"date" < '2019-05-01'
			AND "date" > '2018-11-01') x) y
WHERE
	diff < 60;
'''

g3q = '''

SELECT
	*
FROM (
	SELECT
		comb_score - over_under AS ou_diff,
		hts - ats as odds_diff
	FROM (
		SELECT
			home_team_score + away_team_score AS comb_score,
			over_under,
			home_team_score + odds AS hts,
			away_team_score as ats
		FROM
			games
		WHERE
			"date" < '2019-05-01'
			AND "date" > '2018-11-01') x) y
WHERE
	ou_diff < 60;
'''

g4q = '''

select over_under, abs(odds) as odds from games where 			"date" < '2019-05-01'
			AND "date" > '2018-11-01'

'''


if __name__ == '__main__':

    df = pd.read_sql_query(g2q, actor.conn)
    #print(df)
    sigma = df.std()
    mu = df.mean()
    ax = df.plot.hist(bins=100, alpha=0.5)
    print('asdf')
    print(mu, sigma)
    print('qwer')
    plt.show()

	#this gets a random normal guess for the over under
    print(np.random.normal(mu, sigma, 5))


    
    df = pd.read_sql_query(g3q, actor.conn)
    ax = df.plot.scatter(x='ou_diff', y='odds_diff')
    plt.show()
    
