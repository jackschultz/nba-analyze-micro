from db.db import actor
from .query_strings import team_point_percentages_query


def project_and_insert(date, source, version, user_id):
    full_query = team_point_percentages_query  % (date, source, user_id, version)
    created_info = actor.call_custom_one(full_query)
    print(created_info)
    return created_info['listing_number'], created_info['count']  # only one row returned


def run(date, source, version, user_id):
    print(f"Running projection update: date='{date}', source='{source}', version='{version}', user_id={user_id}")
    # now we need to normalize this.
    listing_number, count = project_and_insert(date, source, version, user_id)
    print(f'Created {count} sub projs of listing number {listing_number}')
    return listing_number, count
