import csv


class Exporter:
    '''
    Class that handles exporting lineups to the format the site expects.
    '''

    def __init__(self, lineups, filename='lineup.csv'):
        self.lineups = lineups
        self.filename = filename


class ExporterFD(Exporter):

    pos_keys = ['PG', 'SG', 'SF', 'PF', 'C']
    headers = ['PG', 'PG', 'SG', 'SG', 'SF', 'SF', 'PF', 'PF', 'C']
    lineup_directory = 'lineups/fd'

    def __init__(self, lineups, filename='fd_lineup.csv'):
        super(ExporterFD, self).__init__(lineups, filename=filename)

    def export(self):
        """
        Exporting the lineups to a csvfile that can be
        uploaded to a site. Currently only FD since
        that's the one I can optimize for now
        """
        with open(f'{self.lineup_directory}/{self.filename}', 'w') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(self.headers)
            lineup_rows = []
            for lineup in self.lineups:
                lineup_rows.append(lineup.row())
            for lineup_row in lineup_rows:
                csv_writer.writerow(lineup_row)

