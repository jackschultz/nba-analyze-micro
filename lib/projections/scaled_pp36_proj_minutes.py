from db.db import actor
from .query_strings import scaled_pp36_proj_minutes_query, scaled_pp36_proj_minutes_0_2_query


def project_and_insert(date, source, version, user_id):
    full_query = scaled_pp36_proj_minutes_0_2_query % (date, source, user_id, version, version)
    created_info = actor.call_custom_one(full_query)
    print(created_info)
    return created_info['listing_number'], created_info['count']  # only one row returned


def run(date, source, version, user_id):
    print(f"Running scaled pp36 proj minutes projection update: date='{date}', source='{source}', version='{version}', user_id={user_id}")
    # now we need to normalize this.
    listing_number, count = project_and_insert(date, source, version, user_id)
    print(f'Created {count} sub projs of listing number {listing_number}')
    return listing_number, count
