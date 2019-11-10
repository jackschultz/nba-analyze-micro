import pandas as pd

from db.db import actor

select_contests_with_date_and_site_str = "select name, date, num_games, min_cash_score, entry_fee, places_paid, max_entrants, total_entrants, min_cash_payout, prize_pool, winning_score, slate, max_entries from contests where date='%s' and site_id=%s"

contest_columns = ['id', 'site_id', 'name', 'date', 'num_games', 'min_cash_score', 'start_time', 'entry_fee', 'places_paid', 'max_entrants', 'total_entrants', 'min_cash_payout', 'prize_pool', 'winning_score', 'slate', 'bulk', 'max_entries']

def get_contests_on_date_for_site(date, site_id):
    query_str = select_contests_with_date_and_site_str % (date, site_id,)
    conn = actor.conn
    df = pd.read_sql_query(query_str, conn)
    return df
