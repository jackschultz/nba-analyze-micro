import psycopg2
#conn = psycopg2.connect(database = "nba", user = "nbauser", password = "nbapassword", host = "localhost", port = "5432")
#cursor = conn.cursor()

url = 'postgres://nbauser:nbauserpassword@localhost:5432/nba'


from psycopg2.pool import ThreadedConnectionPool

min_conns = 1
max_conns = 15
tcp = ThreadedConnectionPool(min_conns, max_conns, url)
