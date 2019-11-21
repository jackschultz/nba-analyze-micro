import calendar
import datetime
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

import asyncio

from db.db import actor

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


versions['0.1-avg-fte-min-01'] = ['set_self_projections_avg_w_fte_minutes', 1]
versions['0.1-avg-fte-min-02'] = ['set_self_projections_avg_w_fte_minutes', 2]
versions['0.1-avg-fte-min-03'] = ['set_self_projections_avg_w_fte_minutes', 3]
versions['0.1-avg-fte-min-05'] = ['set_self_projections_avg_w_fte_minutes', 5]

versions['0.1-avg-dfn-min-03'] = ['set_self_projections_avg_w_dfn_minutes', 3]
versions['0.1-avg-dfn-min-05'] = ['set_self_projections_avg_w_dfn_minutes', 5]

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


async def load_projections_version_on_date(date, sql_fn, limit):
    '''
    Here we're loading or updating the projections from the function specified above that's
    written in the db. Much quicker than using python itself to do the calculations.
    '''
    logger.debug(f'Setting self projections for {date} with function {sql_fn} with limit of {limit}')
    if limit:
        fetched_all = await actor.call_custom_proc(sql_fn, (date,limit,))
    else:
        fetched_all = await actor.call_custom_proc(sql_fn, (date))

    logger.debug(f'Projection responses for {date}, {limit}: {fetched_all}')


async def load_self_projections_for_date(date, versions=versions):
    logger.info(f'Loading {len(versions.keys())} self projections for {date}.')
    for version, _ in versions.items():
        logger.info(f'Loading {version} for {date}...')
        sql_fn, limit = versions[version]
        task = asyncio.create_task(load_projections_version_on_date(date, sql_fn, limit))
        await task
        logger.info(f'Loading {version} completed for {date}')

async def main(date, versions):
    await load_self_projections_for_date(date, versions=versions)


if __name__ == '__main__':



    versions = {}
    #versions['0.1-dfn-min-avg-03'] = ['set_self_projections_dfn_min_avg', 3]
    #versions['0.1-dfn-min-avg-05'] = ['set_self_projections_dfn_min_avg', 5]
    versions['0.1-dfn-min-avg-08'] = ['set_self_projections_dfn_min_avg', 8]

    #versions = {}
    #versions['0.1-dfn-min-ceil-03'] = ['set_self_projections_dfn_min_ceil', 3]
    #versions['0.1-dfn-min-ceil-05'] = ['set_self_projections_dfn_min_ceil', 5]
    versions['0.1-dfn-min-ceil-08'] = ['set_self_projections_dfn_min_ceil', 8]

    #versions = {}
    #versions['0.1-dfn-min-floor-03'] = ['set_self_projections_dfn_min_floor', 3]
    #versions['0.1-dfn-min-floor-05'] = ['set_self_projections_dfn_min_floor', 5]
    versions['0.1-dfn-min-floor-05'] = ['set_self_projections_dfn_min_floor', 8]

    loop = asyncio.get_event_loop()
    date = '2019-11-15'
    loop.run_until_complete(main(date, versions))

    loop.close()
