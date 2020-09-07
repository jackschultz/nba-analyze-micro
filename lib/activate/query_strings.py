
create_self_projections_string = f'''
    insert into projections (stat_line_id, source, user_id)
    (select stat_line_id, '%s', %s from stat_line_calcs where date = '%s');
'''

create_self_projection_subs_string = f'''
    WITH slps AS (
        SELECT
            *
        FROM
            stat_line_projections
        WHERE
            date = '2020-09-03'
            AND source = 'self'
            AND uid = 1
    ),
    inserts AS (
    INSERT INTO projection_subs (projection_id,
            fd_points,
            version,
            listing_number)
    SELECT
        proj_id AS projection_id,
        COALESCE(round(((poss_fd_pct / team_fd_pct_sum) * possible_team_fd_score)::numeric,
        2), 0.00) AS fd_points,
        '0.1-team-pts-pct' AS version,
        (
            SELECT
                coalesce(max(listing_number),
                    0) + 1
            FROM
                projection_subs
            WHERE
                projection_id in(
                    SELECT
                        proj_id FROM slps)) AS listing_number
        FROM (
            SELECT
                sum(poss_fd_pct) OVER (PARTITION BY team_id) team_fd_pct_sum,
                *
            FROM (
            SELECT
                team_setup.*,
                slps.*,
                round(possible_score * fd_point_factor,
                2) AS possible_team_fd_score,
                greatest(random_normal (1,
                proj_fd_pts_pct,
                proj_fd_pts_pct_std) * proj_active::int,
            0) AS poss_fd_pct
            FROM (
            SELECT
                gpvw.*,
                round(expected_score + (random_normal (1,
                gsdvw.avg,
                gsdvw.stddev))::numeric) AS possible_score
            FROM
                games_preview_vw gpvw,
                game_scoring_dist_vw gsdvw) AS team_setup
            JOIN game_point_factors_vw gpfvw ON team_setup.possible_score = gpfvw.team_score
            JOIN slps ON slps.date = team_setup.date
                AND slps.tid = team_setup.team_id) x) y
    RETURNING
        *
    )
    SELECT
        listing_number,
        count(*)
    FROM
        inserts
    GROUP BY
        listing_number;
'''

