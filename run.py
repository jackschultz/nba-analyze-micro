from lib.optimize.base import doit

date = '2020-09-05'
version = '0.2-odds-scaled-med-outside-proj-mins-avg-pp36'
source = 'self'
user_id = 1
site = 'fd'
filename = f'{date}-{version}-3.csv'
filename = None
num_lineups = 10
doit(site, date, source, version, user_id, filename=filename, num_lineups=num_lineups)
