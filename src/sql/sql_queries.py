import pandas as pd
from src.config import engine

ALLOWED_TABLES = {
    'aggr_transaction', 'aggr_user', 'aggr_insurance',
    'map_transaction', 'map_user', 'map_insurance', 
    'top_transaction', 'top_user', 'top_insurance'
}

def fetch_table_data(table_name, year=None, quarter=None):
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"Invalid table name: {table_name}")
    
    query = f"SELECT * FROM {table_name}"
    filters = []
    params = []
    if year is not None:
        filters.append("year = %s")
        params.append(year)
    if quarter is not None:
        filters.append("quarter = %s")
        params.append(quarter)
    if filters:
        query += " WHERE " + " AND ".join(filters)
    return pd.read_sql(query, engine, params=tuple(params))


# Aggregate tables
def get_aggr_transaction(year=None, quarter=None):
    return fetch_table_data("aggr_transaction", year, quarter)

def get_aggr_user(year=None, quarter=None):
    return fetch_table_data("aggr_user", year, quarter)

def get_aggr_insurance(year=None, quarter=None):
    return fetch_table_data("aggr_insurance", year, quarter)

# Map level tables
def get_map_transaction(year=None, quarter=None):
    return fetch_table_data("map_transaction", year, quarter)

def get_map_user(year=None, quarter=None):
    return fetch_table_data("map_user", year, quarter)

def get_map_insurance(year=None, quarter=None):
    return fetch_table_data("map_insurance", year, quarter)

# Top level tables
def get_top_transaction(year=None, quarter=None):
    return fetch_table_data("top_transaction", year, quarter)

def get_top_user(year=None, quarter=None):
    return fetch_table_data("top_user", year, quarter)

def get_top_insurance(year=None, quarter=None):
    return fetch_table_data("top_insurance", year, quarter)