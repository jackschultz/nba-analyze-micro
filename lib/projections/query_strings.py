
# query below needs date, source, user_id, and version in that order for strings
team_point_percentages_query = f'''
    WITH slps AS (
        SELECT
            *
        FROM
            stat_line_projections
        WHERE
            date = '%s'
            AND source = '%s'
            AND uid = %s
    ),
    inserts AS (
    INSERT INTO projection_subs (projection_id,
            fd_points,
            version,
            listing_number)
    SELECT
        proj_id AS projection_id,
        COALESCE(round(((poss_fd_pct / team_fd_pct_sum) * possible_team_fd_score)::numeric,
        2),
    0.00) AS fd_points,
        '%s' AS version,
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

scaled_pp36_proj_minutes_query = f'''
    WITH slps AS (
        SELECT
            *
        FROM
            stat_line_projections
        WHERE
            date = '%s'
            AND source = '%s'
            AND uid = %s
    ),
    inserts AS (
    INSERT INTO projection_subs (projection_id,
            fd_points,
            version,
            listing_number)
    SELECT
        proj_id AS projection_id,
        COALESCE(round(((poss_fd_pts / team_fd_pts_sum) * possible_team_fd_score)::numeric, 2), 0.00) AS fd_points,
        '%s' AS version,
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
                sum(poss_fd_pts) OVER (PARTITION BY team_id) team_fd_pts_sum,
                *
            FROM (
            SELECT
                player_name,
                round(possible_score * fd_point_factor,
                2) AS possible_team_fd_score,
                fd_season_pp36_avg,
                fd_season_pp36_std,
                (greatest(random_normal (1,
                fd_season_pp36_avg,
                fd_season_pp36_std) * proj_active::int,
            0)) * (proj_minutes / 36.0) AS poss_fd_pts,
        slps.proj_minutes,
        team_setup.*,
        slps.*
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

scaled_pp36_proj_minutes_0_2_query = f'''
    WITH slps AS (
        SELECT
            *
        FROM
            stat_line_projections
        WHERE
            date = '%s'
            AND source = '%s'
            AND uid = %s
    ),
    inserts AS (
    INSERT INTO projection_subs (projection_id,
            fd_points,
            version,
            listing_number)
    SELECT
        proj_id AS projection_id,
        COALESCE(round(((poss_fd_pts / team_fd_pts_sum) * possible_team_fd_score)::numeric,
        2),
    0.00) AS fd_points,
        '%s' AS version,
        (
            SELECT
                coalesce(max(listing_number),
                    0) + 1
            FROM
                projection_subs
            WHERE
                projection_id in(
                    SELECT
                        proj_id FROM slps) and "version"='%s') AS listing_number
        FROM (
            SELECT
                sum(poss_fd_pts) OVER (PARTITION BY team_id) team_fd_pts_sum,
                *
            FROM (
            SELECT
                player_name,
                round(possible_score * fd_point_factor,
                2) AS possible_team_fd_score,
                fd_season_pp36_avg,
                fd_season_pp36_std,
                (greatest(random_normal (1,
                fd_season_pp36_avg,
                fd_season_pp36_std) * proj_active::int, 0)) * ((proj_minutes + (select random() * 15 - 4)) / 36.0) AS poss_fd_pts,
                slps.proj_minutes,
        team_setup.*,
        slps.*
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



scaled_pp36_proj_minutes_0_2_query = f'''
    WITH slps AS (
        SELECT
            *
        FROM
            stat_line_projections
        WHERE
            date = '%s'
            AND source = '%s'
            AND uid = %s
    ),
    inserts AS (
    INSERT INTO projection_subs (projection_id,
            fd_points,
            version,
            listing_number)
    SELECT
        proj_id AS projection_id,
        COALESCE(round(((poss_fd_pts / team_fd_pts_sum) * possible_team_fd_score)::numeric,
        2),
    0.00) AS fd_points,
        '%s' AS version,
        (
            SELECT
                coalesce(max(listing_number),
                    0) + 1
            FROM
                projection_subs
            WHERE
                projection_id in(
                    SELECT
                        proj_id FROM slps) and "version"='%s') AS listing_number
        FROM (
            SELECT
                sum(poss_fd_pts) OVER (PARTITION BY team_id) team_fd_pts_sum,
                *
            FROM (
            SELECT
                player_name,
                round(possible_score * fd_point_factor,
                2) AS possible_team_fd_score,
                fd_season_pp36_avg,
                fd_season_pp36_std,
                (greatest(random_normal (1,
                fd_season_pp36_avg,
                fd_season_pp36_std) * proj_active::int, 0)) * ((proj_minutes + (select random() * 15 - 4)) / 36.0) AS poss_fd_pts,
                slps.proj_minutes,
        team_setup.*,
        slps.*
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

scaled_pp36_avg_outside_proj_mins_pp36_query = f'''
    WITH slps AS (
        SELECT
            *
        FROM
            stat_line_projections
        WHERE
            date = '%s'
            AND source = '%s'
            AND uid = %s
    ),
    outside_slps AS (
        SELECT
            oslps.proj_fd_pp36,
            oslps.player_name,
            oslps.pid,
            oslps.proj_minutes
        FROM
            stat_line_projections oslps,
            slps
        WHERE
            slps.slid = oslps.slid
            AND oslps.source in ('dfn', 'rg')
    ),
    outside_avgs AS (
        SELECT
            outside_slps.pid,
            round(avg(proj_fd_pp36),
                2) avg_proj_fd_pp36,
            round(avg(proj_minutes),
                2) avg_proj_minutes
        FROM
            outside_slps
        GROUP BY
            outside_slps.pid
    ),
    inserts AS (
        INSERT INTO projection_subs (projection_id,
                fd_points,
                version,
                listing_number)
    SELECT
        proj_id AS projection_id,
        COALESCE(round(((poss_fd_pts / team_fd_pts_sum) * possible_team_fd_score)::numeric, 2), 0.00) AS fd_points,
        '%s' AS version,
        (
            SELECT
                coalesce(max(listing_number), 0) + 1
            FROM
                projection_subs
            WHERE
                projection_id in(
                    SELECT
                        proj_id FROM slps)
                AND "version" = '%s') AS listing_number
    FROM (
        SELECT
            sum(poss_fd_pts) OVER (PARTITION BY team_id) team_fd_pts_sum,
            *
        FROM (
            SELECT
                player_name,
                round(possible_score * fd_point_factor, 2) AS possible_team_fd_score,
                oa.avg_proj_fd_pp36,
                fd_season_pp36_std, -- keep this season long because 
                (greatest(random_normal (1, oa.avg_proj_fd_pp36, fd_season_pp36_std) * proj_active::int, 0)) * ((oa.avg_proj_minutes + ( SELECT random() * 10 - 5)) / 36.0) AS poss_fd_pts_old,
                 (greatest(random_normal (1, oa.avg_proj_fd_pp36, fd_season_pp36_std - (0.15 * fd_season_pp36_std)) * proj_active::int, 0)) * ((oa.avg_proj_minutes) / 36.0) AS poss_fd_pts,
                oa.avg_proj_minutes,
               team_setup.*,
               slps.*
            FROM (
                SELECT
                    gpvw.*,
                    round(expected_score + (random_normal (1, gsdvw.avg, gsdvw.stddev))::numeric) AS possible_score
                FROM
                    games_preview_vw gpvw,
                    game_scoring_dist_vw gsdvw) AS team_setup
                    JOIN game_point_factors_vw gpfvw ON team_setup.possible_score = gpfvw.team_score
                    JOIN slps ON slps.date = team_setup.date
                                AND slps.tid = team_setup.team_id
                    JOIN outside_avgs oa on oa.pid = slps.pid) x) y
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