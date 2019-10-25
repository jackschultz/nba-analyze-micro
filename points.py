import pandas as pd
import matplotlib.pyplot as plt


from db import conn

query_str = "select fd_salary, round(avg(fd_points), 2) as pts, count(*) from stat_line_points where minutes > 0 and fd_salary is not null and fd_salary > 0 group by fd_salary;"

query_str = 'select fd_salary, fd_points from stat_line_points where minutes > 0 and fd_salary is not null;'

df = pd.read_sql_query(query_str, conn)

print(df)

plt.figure()

bp = df.boxplot(column='fd_points', by='fd_salary')

plt.show()