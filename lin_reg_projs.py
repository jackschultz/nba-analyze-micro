from db.db import actor


coeffs = {'avg_prev5_minutes': 0.0463433544725511,
          'avg_prev10_minutes': -0.11827739667632739,
          'fd_avg_prev5_pp36': 0.13325681882277532,
          'fd_avg_prev10_pp36': 0.5375229590158227,
          'fd_std_prev5_pp36': 0.1302018794438968,
          'fd_std_prev10_pp36': 0.22013652492158264,
          'home': 0.8231458145546704,
          'team_b2b': -0.5840017842772196,
          'opp_b2b': 0.46572937077292326,
          'team_l5_wins': -0.2868507424566815,
          'opp_l10gpace': 0.003898371239450648,
          'opp_l5gpg': 0.0161173674040293,
          'opp_l10gpg': 0.045161307097170894,
          'opp_l8_wins': -0.07230770233161384,
          'opw_l10_pp36_given_pos': 0.17677990717565795}


q = 'select * from test_proj_view where "date"=%s'

def set_lin_reg_projections(date, version):
    qwer = actor.call_custom_all(q, (date,))

    import decimal
    from collections import defaultdict
    projs = defaultdict(lambda: 0)
    for sl in qwer:
        slid = sl['stat_line_id']
        for key, val in coeffs.items():
            try:
                projs[slid] += decimal.Decimal(val) * sl[key]
            except Exception as e:
                import pdb;pdb.set_trace()
                asdf = 5

    source = 'self'
    for slid, fdpp36 in projs.items():
        actor.create_or_update_fd_projection(slid, source, {}, None, None, fdpp36, version)



def combine_self_lin_reg_and_minutes(date, version_pp36, version_min, new_version_name):
    """Going through the projections that are 0.2-lin-reg and matching them up
       with projections for the same stat_line and that have minute projections"""
    print(f'Combining {version_pp36} with {version_min} minutes to {new_version_name}')
    query = 'select * from projections where stat_line_id=%s and version=%s'
    slps = actor.find_stat_line_points_on_date(date)
    for slp in slps:
        slid = slp['stat_line_id']
        proj_pp36 = actor.call_custom_one(query, (slid, version_pp36,))
        proj_min = actor.call_custom_one(query, (slid, version_min,))
        if proj_pp36 and proj_min: #meaning that they fit the criteria for prediction, moslty by average minutes before.
            fd_points = proj_pp36['fdpp36'] * (proj_min['minutes'] / 36)
            actor.create_or_update_fd_projection(slid, 'self', {}, proj_min['minutes'], fd_points, None, new_version_name)


minute_versions = ['0.1-dfn', '0.1-fte', '0.1-rg']

#####
# Before running make sure to refresh views
# TODO put that in a function
# `refresh materialized view stat_line_windows;`
# `refresh materialized view team_points_windows;`
#####
if __name__ == '__main__':
    version_pp36 = '0.2-lin-reg'
    date = '2019-11-15'
    set_lin_reg_projections(date, version_pp36)

    for version_min in minute_versions:
        minute_site = version_min.split('-')[1]
        new_version_name = f'0.2-lin-reg-{minute_site}-min'
        combine_self_lin_reg_and_minutes(date, version_pp36, version_min, new_version_name)

