import decimal
from collections import defaultdict

from db.db import actor
import utils


coeffs = {'avg_prev5_minutes': 0.022111461792515254,
          'avg_prev10_minutes': -0.10079320554600223,
          'fd_avg_prev5_pp36': 0.13256729048761273,
          'fd_avg_prev10_pp36': 0.5182241883191786,
          'fd_std_prev5_pp36': 0.12073393632473829,
          'fd_std_prev10_pp36': 0.18845500235037754,
          'home': 0.872277329008171,
          'team_b2b': -0.5648345283549704,
          'opp_b2b': 0.6593120672292039,
          'team_l5_wins': -0.2511291131500383,
          'opp_l10gpace': 0.04438330785528479,
          'opp_l5gpg': 0.018735095783172347,
          'opp_l10gpg': 0.04142048011933274,
          'opp_l8_wins': -0.03549706287885674,
          'opw_l10_pp36_given_pos': 0.16898319556950248}

intercept = decimal.Decimal(-11.15)

q = 'select * from test_proj_view where "date"=%s'

def set_lin_reg_projections(date, version):
    print(f'Setting Lin Reg projections {version} for {date}')
    qwer = actor.call_custom_all(q, (date,))

    import decimal
    from collections import defaultdict
    projs = defaultdict(int)
    for sl in qwer:
        slid = sl['stat_line_id']
        projs[slid] = intercept
        for key, val in coeffs.items():
            try:
                projs[slid] += decimal.Decimal(val) * sl[key]
            except Exception as e:
                import pdb;pdb.set_trace()
                asdf = 5

    source = 'self'
    for slid, fdpp36 in projs.items():
        actor.create_or_update_fd_projection(slid, source, bulk={}, fdpp36=fdpp36, version=version)



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
        fd_salary = slp['fd_salary']

        if proj_pp36 and proj_min: #meaning that they fit the criteria for prediction, moslty by average minutes before.
            fd_points = proj_pp36['fdpp36'] * (proj_min['minutes'] / 36)
            proj_pp36_num = proj_pp36['fdpp36']
            fd_value = utils.get_self_value(fd_salary, float(proj_pp36_num))
            actor.create_or_update_fd_projection(slid, 'self', bulk={}, minutes=proj_min['minutes'], fd_points=fd_points, fdpp36=proj_pp36_num, version=new_version_name, fd_value=fd_value)


def set_and_combine_for_date(date):
    set_lin_reg_projections(date, version_pp36)

    for version_min in minute_versions:
        minute_site = version_min.split('-')[1]
        new_version_name = f'{version_pp36}-{minute_site}-min'
        combine_self_lin_reg_and_minutes(date, version_pp36, version_min, new_version_name)




minute_versions = ['0.1-dfn', '0.1-fte', '0.1-rg']

#####
# Before running make sure to refresh views
# TODO put that in a function
# `refresh materialized view stat_line_windows;`
# `refresh materialized view team_points_windows;`
#####
if __name__ == '__main__':
    version_pp36 = '0.2-lin-reg'
    dates = ['2019-11-19', '2019-11-18', '2019-11-17', '2019-11-16', '2019-11-15', '2019-11-14','2019-11-13','2019-11-12','2019-11-11','2019-11-10','2019-11-09','2019-11-08']
    dates = ['2019-11-20']
    for date in dates:
        set_and_combine_for_date(date)

