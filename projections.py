from lib.projections.team_point_percentages import run as run_team_point_percentages


if __name__ == '__main__':
    site = 'fd'
    date = '2020-09-03'
    source = 'self'
    version = '0.1-team-pts-pct'
    user_id = 1

    run_team_point_percentages(date, source, version, user_id)
