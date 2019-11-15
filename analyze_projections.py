import pandas as pd
import numpy as np  
from sklearn.model_selection import train_test_split 

from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, \
                                 Lars, OrthogonalMatchingPursuit, BayesianRidge, \
                                 ARDRegression, SGDRegressor, PassiveAggressiveRegressor, \
                                 RANSACRegressor, TheilSenRegressor, HuberRegressor

from sklearn import metrics
'''
import matplotlib.pyplot as plt  
import seaborn as seabornInstance 

'''

from db.db import actor

query = '''

SELECT
	fd_act_pp36,
	avg_prev5_minutes,
	--avg_prev8_minutes,
	avg_prev10_minutes,
	fd_avg_prev5_pp36,
	--fd_avg_prev8_pp36,
	fd_avg_prev10_pp36,
	fd_std_prev5_pp36,
	--fd_avg_prev8_pp36,
	fd_std_prev10_pp36,
	home,
	tpw.b2b as team_b2b,
    opw.b2b as opp_b2b,

	--tpw.l5gps as team_l5gps,
	--tpw.l8gps as team_l8gps,
	--tpw.l10gps as team_l10gps,
	
	--tpw.l5gpace as team_l5gpace,
	--tpw.l8gpace as team_l8gpace,
	--tpw.l10gpace as team_l10gpace,
	
	--tpw.l5gpg as team_l5gpg,
	--tpw.l8gpg as team_l8gpg,
	--tpw.l10gpg as team_l10gpg,
		
	tpw.l5_wins as team_l5_wins,
	--tpw.l8_wins as team_l8_wins,
	--tpw.l10_wins as team_l10_wins,
	
	--opw.l5gps as opp_l5gps,
	--opw.l8gps as opp_l8gps,
	--opw.l10gps as opp_l10gps,
	
	--opw.l5gpace as opp_l5gpace,
	--opw.l8gpace as opp_l8gpace,
	opw.l10gpace as opp_l10gpace,
	
	opw.l5gpg as opp_l5gpg,
	--opw.l8gpg as opp_l8gpg,
	opw.l10gpg as opp_l10gpg,

	--opw.l5_wins as opp_l5_wins,
	opw.l8_wins as opp_l8_wins,
	--opw.l10_wins as opp_l10_wins,

    /*
	CASE WHEN slw.fd_positions like 'PG' THEN opw.l8_fd_pts_given_pg
	    	WHEN slw.fd_positions like 'SG' THEN opw.l8_fd_pts_given_sg
	    	WHEN slw.fd_positions like 'SF' THEN opw.l8_fd_pts_given_sf
	    	WHEN slw.fd_positions like 'PF' THEN opw.l8_fd_pts_given_pf
	    	WHEN slw.fd_positions like 'C' THEN opw.l8_fd_pts_given_c
	END as opw_pts_given_pos,
    */

    /*
	CASE WHEN slw.fd_positions like 'PG' THEN opw.l5_fd_pp36_given_pg
	    	WHEN slw.fd_positions like 'SG' THEN opw.l5_fd_pp36_given_sg
	    	WHEN slw.fd_positions like 'SF' THEN opw.l5_fd_pp36_given_sf
	    	WHEN slw.fd_positions like 'PF' THEN opw.l5_fd_pp36_given_pf
	    	WHEN slw.fd_positions like 'C' THEN opw.l5_fd_pp36_given_c
	END as opw_l5_pp36_given_pos,
    */

	/*
    CASE WHEN slw.fd_positions like 'PG' THEN opw.l8_fd_pp36_given_pg
	    	WHEN slw.fd_positions like 'SG' THEN opw.l8_fd_pp36_given_sg
	    	WHEN slw.fd_positions like 'SF' THEN opw.l8_fd_pp36_given_sf
	    	WHEN slw.fd_positions like 'PF' THEN opw.l8_fd_pp36_given_pf
	    	WHEN slw.fd_positions like 'C' THEN opw.l8_fd_pp36_given_c
	END as opw_l8_pp36_given_pos,
    */

	CASE WHEN slw.fd_positions like 'PG' THEN opw.l10_fd_pp36_given_pg
	    	WHEN slw.fd_positions like 'SG' THEN opw.l10_fd_pp36_given_sg
	    	WHEN slw.fd_positions like 'SF' THEN opw.l10_fd_pp36_given_sf
	    	WHEN slw.fd_positions like 'PF' THEN opw.l10_fd_pp36_given_pf
	    	WHEN slw.fd_positions like 'C' THEN opw.l10_fd_pp36_given_c
	END as opw_l10_pp36_given_pos
	

FROM
	stat_line_windows slw,
	team_points_windows tpw,
	team_points_windows opw -- opponent's info
WHERE
	slw. "date" = tpw. "date"
	AND slw.team_id = tpw.team_id
	AND tpw.opponent_id = opw.team_id
	AND opw."date" = slw."date"
	AND valid5
	AND valid8
	AND valid10
	AND active
	AND act_minutes > 15
	AND ((slw."date" > '2018-11-05' AND slw."date" < '2019-04-22')
        OR (slw."date" > '2017-11-05' AND slw."date" < '2018-04-22')
        OR (slw."date" > '2016-11-05' AND slw."date" < '2017-04-22')
    );
'''


conn = actor.conn
df = pd.read_sql_query(query, conn)

df = df.fillna(method='ffill')

print(df)

X = df.drop('fd_act_pp36', axis=1).values
y = df['fd_act_pp36'].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=0)


regressor = ElasticNet(alpha=0.1)
regressor = Lars()
regressor = Lasso(alpha=0.001) 
regressor = Ridge()
regressor = LinearRegression(normalize=True) 


regressor.fit(X_train, y_train) #training the algorithm


coeff_df = pd.DataFrame(regressor.coef_, df.columns[1:], columns=['Coefficient']) 

y_pred = regressor.predict(X_test)

df2 = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})
df3 = df2.head(25)

pd.options.display.float_format = '{:.8f}'.format
print(coeff_df)
print(coeff_df.to_dict())

print('FD Point MEan:', df['fd_act_pp36'].mean())
print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))  
print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))  
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))

