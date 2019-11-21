import csv

fd_pos_keys = ['PG', 'SG', 'SF', 'PF', 'C']
fd_headers = ['PG', 'PG','SG', 'SG', 'SF', 'SF', 'PF', 'PF', 'C']

def lineup_rows(lineups):
    pass

def export_lineups(lineups, filename='lineups.csv'):
    """Exporting the lineups to a csvfile that can be
       uploaded to a site. Currently only FD since
       that's the one I can optimize for now"""
    with open(f'lineups/{filename}', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(fd_headers)
        lineup_rows = []
        for lineup in lineups:
            lineup_row = []
            for key in fd_pos_keys:
                lineup_row.extend(lineup[key])
            lineup_rows.append(lineup_row)
        for lineup_row in lineup_rows:
            csv_writer.writerow(lineup_row)

