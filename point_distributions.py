import pandas as pd
from db.db import tcp
import matplotlib.pyplot as plt


query_string = '''
	SELECT
		(slp.fdpp36 - proj.fdpp36) AS diff,
		version
	FROM
		projections proj,
		stat_line_points slp
	WHERE
		"source" = 'self'
		AND proj.stat_line_id = slp.stat_line_id
		AND proj.fdpp36 IS NOT NULL
		AND slp.fdpp36 IS NOT NULL
		AND slp.minutes > 10
		AND proj.fdpp36 < 200
		AND proj.version = '0.1-avg-fte-min-03'
        AND proj."source"='self';
'''

if __name__ == '__main__':
    conn = tcp.getconn()
    df = pd.read_sql_query(query_string, conn)
    tcp.putconn(conn)
    print(df)

    ax = df.plot.hist(bins=100, alpha=0.5)
    plt.show()
