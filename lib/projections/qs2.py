
insert_query_string = '''
    INSERT INTO projection_subs (projection_id,
            fd_points,
            version,
            listing_number)
'''


template_query_string = '''
    WITH slps AS (
        SELECT
            *
        FROM
            stat_line_projections
        WHERE
            date = {{ date }}
            AND source = {{ source }}
            AND uid = {{ user_id }}
    ),
    slpos AS (
        -- stat_line_projection_others
        SELECT
            slid,
            round(avg(proj_fd_pp36),
                2) avg_proj_pp36,
            round(avg(proj_minutes),
                2) avg_proj_minutes,
            PERCENTILE_DISC(0.5)
            WITHIN GROUP (ORDER BY proj_minutes) med_proj_minutes
        FROM
            stat_line_projections
        WHERE
            date = {{ date }}
            AND source in('dfn',
                'rg',
                'nf')
        GROUP BY
            slid
    ),
    team_setup AS (
        SELECT
            gpvw.*,
            round(expected_score + (random_normal (1, gsdvw.avg, gsdvw.stddev))::numeric) AS possible_score
        FROM
            games_preview_vw gpvw, game_scoring_dist_vw gsdvw
        WHERE
            gpvw.date = {{ date }}
    ) 
    SELECT
        slps.proj_id projection_id, -- key projection id for the insert
        slps.slid,
        slps.fd_season_pp36_avg,
        slps.fd_season_pp36_std,
        slpos.avg_proj_pp36,
        slpos.avg_proj_minutes,
        slpos.med_proj_minutes,
        slps.player_name,
        ts.*,
        gpfvw.fd_point_factor * ts.possible_score as poss_team_fd_points,
        (
            SELECT
                coalesce(max(listing_number), 0) + 1
            FROM
                projection_subs
            WHERE
                projection_id in(
                    SELECT
                        proj_id FROM slps)
                AND "version" = {{ version }}) AS listing_number
    FROM
        slps
        JOIN slpos ON slps.slid = slpos.slid
        JOIN team_setup ts ON slps.tid = ts.team_id
        JOIN game_point_factors_vw gpfvw on gpfvw.team_score = ts.possible_score
    ORDER BY med_proj_minutes desc;
'''