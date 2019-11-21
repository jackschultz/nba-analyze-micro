import pandas as pd
from db.db import actor
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.linear_model import LinearRegression



query_string = '''
SELECT
	--slp.fd_points - proj_self.fd_points as self_diff
	--slp.fd_points - proj_dfn.fd_points as dfn_diff,
    slp.team_id,
    slp.minutes,
    proj_self.minutes as min_self_proj,
	slp.fdpp36 - (proj_self.fd_points / (proj_self.minutes / 36)) as pp36_self_proj,
	slp.fdpp36 - (proj_dfn.fd_points / (proj_dfn.minutes / 36)) as pp36_dfn_proj,
    slp.fdpp36 - (proj_rg.fd_points / (proj_rg.minutes / 36)) as pp36_rg_proj
FROM

	projections proj_self,
	projections proj_dfn,
    projections proj_rg,
	stat_line_points slp
WHERE
	proj_self.stat_line_id = slp.stat_line_id
	AND proj_dfn.stat_line_id = slp.stat_line_id
	AND proj_rg.stat_line_id = slp.stat_line_id
	AND slp.active
	AND slp.fd_points > 0
	AND slp.minutes > 15
	--AND slp.fd_salary >= 8000
	--AND slp.fd_salary < 9000
	AND proj_self.minutes > 10
	AND proj_dfn.minutes > 10
	AND proj_dfn.version = '0.1-dfn'
    AND proj_rg.version = '0.1-rg'
	AND proj_self.version = '0.2-lin-reg-dfn-min'
	AND slp."date">'2019-11-07';
'''

q2 = '''
	SELECT
		slp.fdpp36
	FROM
		stat_line_points slp
	WHERE
		--proj.stat_line_id = slp.stat_line_id
		slp.active
		AND slp.fd_points > 0
		AND slp.minutes > 15
        AND slp.fd_salary > 4000
        AND slp.fd_salary < 5000
		--AND proj.version = '0.2-lin-reg'
		AND slp. "date" > '2018-10-01';
'''

q3 = '''
select sal, avgpp36 from fd_sal_stats where sal >= 3500 and sal < 12000;
'''

q4 = '''
select avg_diff from (
SELECT
	proj.fd_value,
	proj.fd_points,
	slp.fd_points,
	proj.fd_points - slp.fd_points as act_diff,
	slp.fd_points - fss.aver as avg_diff
FROM
	projections proj,
	stat_line_points slp,
	fd_sal_stats fss
WHERE
	proj.stat_line_id = slp.stat_line_id
	AND fss.sal = slp.fd_salary
	AND slp. "date" > '2019-11-11'
	AND slp."date" < '2019-11-18'
	AND proj. "version" = '0.2-lin-reg-dfn-min'
	AND slp.fd_salary > 3400
	AND proj.fd_points > 20
	AND proj.minutes > 15
	AND proj.fd_value > 1.7
	AND slp.active
	)x;

'''

if __name__ == '__main__':

    df = pd.read_sql_query(q4, actor.conn)
    #print(df)
    print(len(df))
    print('stds')
    print(df.std())
    print('avgs')
    print(df.mean())

    ax = df.plot.hist(bins=10, alpha=0.5)
    plt.show()



    '''
    df = pd.read_sql_query(q2, actor.conn)
    #print(df)
    print(len(df))
    print('stds')
    print(df.std())
    print('avgs')
    print(df.mean())

    import pdb;pdb.set_trace()

    ax = df.plot.hist(bins=100, alpha=0.5)
    plt.show()

    '''
    '''

    #array([[0.00335557]])
    #array([13.78824624])

    #predicting salary from pp36
    #array([[293.42862071]])
    #array([-3927.43704516])
    '''
    '''
    df = pd.read_sql_query(q3, actor.conn)
    print(df)

    Y = df['sal'].values.reshape(-1, 1)
    X = df['avgpp36'].values.reshape(-1, 1)

    regressor = LinearRegression()
    regressor.fit(X, Y)

    import pdb;pdb.set_trace()
    ax = df.plot.scatter(x='avgpp36', y='sal')
    plt.show()
    '''
