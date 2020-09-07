from .calculate import solve
from .finders import get_stat_lines_for_date, get_actual_points_sal_for_ids

from ndba.models import Lineup
from db.db import actor

import numpy as np

class ProjectionError(Exception):
    def __init__(self, errvals):
        self.errvals = errvals

class ProjectionOptimizer:
    '''
    Class that performs optimization and returns the best linupe
    based on projections provided.

    Attributes
    __________
    site : str
        abbreviation of the site for this projection optimizer.
        eg: 'fd', 'dk'
    date : str
        date abbrv for the date of this projections
        eg: '2020-01-21'
    projections : dataframe
        pandas dataframe with the following columns:
            pid  : player_id in the database
            name : player's name
            pos  : player's positions on the site
            sal  : player's salaries
            pts  : player's projected points
    includes : list
        dataframe in same format as above, of players who are included in this lineup.
        This can be used as a way to make sure you include players, such as Giannis,
        no matter what their projection number is.

    '''
    def __init__(self, site, date, projections, includes=[]):
        self.date = date
        self.site = site
        self.projections = projections
        self.includes = includes
        self.combo_positions_dict = {'PG': 2, 'SG': 2, 'SF': 2, 'PF': 2, 'C': 1}
        self.combo_salary = 0

    def optimize(self):
        pass

class ProjectionOptimizerDK(ProjectionOptimizer):
    pass

class ProjectionOptimizerFD(ProjectionOptimizer):

    max_salary = 60000

    def __init__(self, date, projections, includes=[]):
        self.date = date
        self.site = 'fd'
        self.projections = projections
        self.includes = includes

        self.combo_positions_dict = {'PG': 2, 'SG': 2, 'SF': 2, 'PF': 2, 'C': 1}
        self.combo_salary = 0
        self.players = []
        self.includes_stat_line_points = {}
        # probably a better way to do this validation...
        self.validate_and_load_input()

    def validate_and_load_input(self):

        errors = []

        matches = set(self.includes)
        if len(matches) > 0:
            message = 'Same players id(s) in both include and exclude'
            ids = list(matches)
            errors.append({'message': message, 'vals': ids, 'code': 400})

        message = 'Some included players do not play on this date.'
        vals = []
        for pid in self.includes:
            #find the player and make sure he has a stat line for that date
            slpi = actor.find_stat_line_by_player_and_date(pid, self.date)
            if not slpi:
                vals.append(pid)
            else:
                # Now we can add the players as well
                self.includes_stat_line_points[pid] = slpi
                self.combo_salary += slpi['fd_salary']
                self.combo_positions_dict[slpi['fd_positions']] -= 1

        if self.invalid_combo_positions():
            message = f'Too many players of the same position included.'
            errors.append({'message': message, 'code': 400})

        if vals:
            print(vals)
            errors.append({'message': message, 'vals': vals, 'code': 400})

        if len(errors) > 0:
            raise ProjectionError(errors)

        return None

    @classmethod
    def save(cls, lineup, site_id, user_id, date, version, listing_number):
        '''
        Saves optimized lineup to the db
        '''
        player_infos = lineup.player_db_infos()
        db_lineup = actor.session.query(Lineup).filter(Lineup.date==date, Lineup.user_id==user_id, Lineup.version==version, Lineup.listing_number==listing_number).first()
        if not db_lineup:
            db_lineup = Lineup(user_id=user_id, date=date, version=version, listing_number=listing_number)
        db_lineup.site_id = site_id
        db_lineup.player_infos = player_infos
        actor.session.add(db_lineup)
        actor.session.commit()
        return db_lineup.id

    def load(self):
        pass


    def player_db_infos(self):
        selected_player_ids = [p['pid'] for p in self.players]
        retval = self.projections[self.projections['pid'].isin(selected_player_ids)].to_dict('records')
        return retval

    def row(self):
        """
        Row of the positions for lineup csvs
        """
        retval = []
        retval.extend([x['site_id'] for x in self.players if x['pos'] == 'PG'])
        retval.extend([x['site_id'] for x in self.players if x['pos'] == 'SG'])
        retval.extend([x['site_id'] for x in self.players if x['pos'] == 'SF'])
        retval.extend([x['site_id'] for x in self.players if x['pos'] == 'PF'])
        retval.extend([x['site_id'] for x in self.players if x['pos'] == 'C'])
        return retval

    def remaining_position_dict(self):
        return self.combo_positions_dict

    def remaining_salary(self):
        return ProjectionOptimizerFD.max_salary - self.combo_salary

    def invalid_combo_positions(self):
        return any(val < 0 for val in [value for key, value in self.combo_positions_dict.items()])

    def valid_combo_salary(self):
        return self.combo_salary <= ProjectionOptimizerFD.max_salary

    def possible_stat_lines(self, version):
        '''
        This df includes the included values. We need this because in the end,
        we need to get the info about that player with that id.
        '''
        return get_stat_lines_for_date(self.date)


    def optimize(self):
        '''
        Optimize the remaining parts of the lineup based on the projections
        df needs
        '''
        #df = self.possible_stat_lines(version)
        df = self.projections # only to make this shorter

        #if df.empty:
        #    raise(ProjectionError({'message': 'Database returned no players to optimize with.'}))

        solve_df = df[~df.pid.isin(self.includes)]
        fin = solve(self.combo_positions_dict, self.remaining_salary(), solve_df)

        winner = fin[1]

        includes_df_indexes = df.loc[df['pid'].isin(self.includes)]

        if not includes_df_indexes.empty:
            winning_ids = np.hstack([winner[-1], includes_df_indexes.index.values])
        else:
            winning_ids = winner[-1]

        top_players = df.iloc[winning_ids]

        print("\n")
        print(top_players)

        print("\n")
        print("Combined player points:", sum(df.iloc[winning_ids].pts))
        print("Combined player salary:", sum(df.iloc[winning_ids].sal))
        print("Combined actual points:", sum(df.iloc[winning_ids].act_pts))
        print("\n")

        projected_salary = sum(df.iloc[winning_ids].sal)
        projected_points = sum(df.iloc[winning_ids].pts)

        retval = {}

        projections = {}
        projections['salary'] = projected_salary
        projections['points'] = projected_points
        retval['projections'] = projections

        top_pids = top_players['pid'].to_list()
        actual_points, actual_salary = get_actual_points_sal_for_ids(
            top_pids, self.date)
        actuals = {}
        actuals['salary'] = actual_salary
        actuals['points'] = actual_points
        retval['actuals'] = actuals

        top_player_projections = top_players.to_dict('records')
        top_pid_stat_lines = actor.find_stat_line_points_on_date_for_player_ids(self.date, tuple(top_pids))

        retval['players'] = top_player_projections
        self.players = top_player_projections

        return retval
