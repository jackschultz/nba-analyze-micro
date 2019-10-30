import calendar
import datetime

from concurrent.futures import ThreadPoolExecutor

from db.db import tcp

versions = {}
versions['0.1-avg-01']  = ['set_self_projections_avg', 1]
versions['0.1-avg-02']  = ['set_self_projections_avg', 2]
versions['0.1-avg-03']  = ['set_self_projections_avg', 3]
versions['0.1-avg-05']  = ['set_self_projections_avg', 5]
versions['0.1-avg-08']  = ['set_self_projections_avg', 8]
versions['0.1-avg-10'] = ['set_self_projections_avg', 10]
versions['0.1-avg-12'] = ['set_self_projections_avg', 12]


versions['0.1-med-01']  =  ['set_self_projections_med', 1]
versions['0.1-med-02']  =  ['set_self_projections_med', 2]
versions['0.1-med-03']  =  ['set_self_projections_med', 3]
versions['0.1-med-05']  =  ['set_self_projections_med', 5]
versions['0.1-med-08']  =  ['set_self_projections_med', 8]
versions['0.1-med-10'] = ['set_self_projections_med', 10]
versions['0.1-med-12'] = ['set_self_projections_med', 12]


versions['0.1-std-ceil-05']  = ['set_self_projections_std_ceil', 5]
versions['0.1-std-ceil-08']  = ['set_self_projections_std_ceil', 8]
versions['0.1-std-ceil-10'] = ['set_self_projections_std_ceil', 10]
versions['0.1-std-ceil-12'] = ['set_self_projections_std_ceil', 12]

versions['0.1-avg-actual-03'] = ['set_self_projections_avg_score', 3]
versions['0.1-avg-actual-05'] = ['set_self_projections_avg_score', 5]
versions['0.1-avg-actual-08'] = ['set_self_projections_avg_score', 8]


def iso_dates_in_month(year, month):
    '''
    Yields date in isoformat in a specific year and month
    '''
    num_days = calendar.monthrange(year, month)[1]
    days = [datetime.date(year, month, day) for day in range(1, num_days+1)]
    for day in days:
        yield day.isoformat()


def loop_months_for_season():
    combos = []
    #combos.append([2019, [10,11,12]])
    combos.append([2019, [10]])
    #combos.append([2020, [1,2,3,4,5,6]])
    for year, months in combos:
        for month in months:
            yield (year, month)


def load_projections_version_on_date(date, sql_fn, limit):
    '''
    Here we're loading or updating the projections from the function specified above that's
    written in the db. Much quicker than using python itself to do the calculations.
    '''
    print(f'Setting self projections for {date} with limit {limit}')
    conn = tcp.getconn()
    cursor = conn.cursor()

    if limit:
        cursor.callproc(sql_fn, (date,limit))
    else:
        cursor.callproc(sql_fn, (date))
    conn.commit()
    fetched_all = cursor.fetchall()
    print(f'res for {date}, {limit}: {fetched_all}')
    tcp.putconn(conn)


'''
for version, _ in versions.items():
    with ThreadPoolExecutor(max_workers=15) as executor:
        for year, month in loop_months_for_season():
            for date in iso_dates_in_month(year, month):
                sql_fn, limit = versions[version]
                print(date, sql_fn, limit)
                executor.submit(load_projections_version_on_date, date, sql_fn, limit)
'''


def load_self_projections_for_date(date, versions=versions):
    with ThreadPoolExecutor(max_workers=15) as executor:
        for version, _ in versions.items():
            sql_fn, limit = versions[version]
            print(date, sql_fn, limit)
            executor.submit(load_projections_version_on_date, date, sql_fn, limit)

if __name__ == '__main__':

    date = '2019-10-28'
    load_self_projections_for_date(date)
