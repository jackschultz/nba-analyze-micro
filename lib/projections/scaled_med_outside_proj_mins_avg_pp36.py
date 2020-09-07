from db.db import actor
from .qs2 import template_query_string
from ndba.models import ProjectionSub

import numpy as np
import pandas as pd
from jinjasql import JinjaSql
j = JinjaSql()


def project_and_insert(date, source, version, user_id):
    sql_template_data = {'date': date, 'source': source, 'user_id': user_id, 'version': version}
    query, bind_params = j.prepare_query(template_query_string, sql_template_data)

    df = pd.read_sql_query(query, actor.conn, params=bind_params)

    row_count = df.shape[0]
    df['rand_pp36'] = np.random.normal(df['avg_proj_pp36'], df['fd_season_pp36_std'], row_count)
    df['poss_fd_points'] = df['rand_pp36'] * (df['med_proj_minutes'] / 36.0)
    df['version'] = version

    # putting the team point totals here
    df['team_point_sum'] = df.groupby('team_id')['poss_fd_points'].transform('sum')

    df['fd_points'] = df['poss_fd_points'] * (df['poss_team_fd_points'] / df['team_point_sum'])

    projection_subs_df = df[['projection_id', 'fd_points', 'version', 'listing_number']]

    for index, row in projection_subs_df.iterrows():
        ps_data = row.to_dict()
        ps = ProjectionSub(**ps_data)
        actor.session.add(ps)
    actor.session.commit()

    listing_number = int(df.listing_number.unique()[0])
    print(projection_subs_df)

    return listing_number, row_count


def run(date, source, version, user_id):
    print(f"Running scaled pp36 proj minutes projection update: date='{date}', source='{source}', version='{version}', user_id={user_id}")
    # now we need to normalize this.
    listing_number, count = project_and_insert(date, source, version, user_id)
    print(f'Created {count} sub projs of listing number {listing_number}')
    return listing_number, count
