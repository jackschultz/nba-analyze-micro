import numpy as np

#we're assuming the mean is 0, since it's very close in the ~0.1 range
odds_std = 12.843645
over_under_std = 17.637512



def possible_score(odds, over_under):
    pass
    odds_rand = np.random.normal(0, odds_std, 1)
    over_under_rand = np.random.normal(0, over_under_std, 1)
    total_score = over_under + over_under_rand # meaning this will be the accepted total score.
    new_odds = odds + odds_rand
    # let's say odds are -6, and the rand is 0. That means the hts - awt needs to equal 9
    # since the value for total_score is 200. Then the hts is 103, ats = 97, where home team
    # wins by 6 and total score is 200. This means that we subtract the new odds from the
    # total_score / 2 since odds are negative for the team that scores more.
    hts = (total_score / 2.0) - (new_odds / 2.0)
    ats = (total_score / 2.0) + (new_odds / 2.0)
    return hts, ats

if __name__ == '__main__':

    # testing that the scores come out in the correct way with many iterations.

    score_diffs = []
    tot_scores = []
    for i in range(10000):
        hts, ats = possible_score(-4.5, 220)
        score_diffs.append(hts - ats)
        tot_scores.append(ats + hts)
    a = np.array(score_diffs)
    b = np.array(tot_scores)

    print(f'Mean: {np.mean(a)}')
    print(f'STD: {np.std(a)}')

    print(f'Mean: {np.mean(b)}')
    print(f'STD: {np.std(b)}')

