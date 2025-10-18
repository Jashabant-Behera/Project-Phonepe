import pandas as pd
from src.config import engine

class PhonePeAnalytics:
    """SQL queries for PhonePe business analytics"""
    
    def __init__(self):
        self.engine = engine
    
    # ============ SUMMARY DASHBOARDS ============
    
    def get_executive_summary(self, year=None, quarter=None):
        """Get executive summary metrics"""
        filters = []
        params = []
        
        if year:
            filters.append("year = %s")
            params.append(year)
        if quarter:
            filters.append("quarter = %s")
            params.append(quarter)
        
        where_clause = " WHERE " + " AND ".join(filters) if filters else ""
        params_tuple = tuple(params) if params else None
        
        # Transactions - Use COALESCE to handle NULL
        trans_query = f"""
            SELECT 
                COALESCE(SUM(trans_amount), 0) as total_transaction_amount,
                COALESCE(SUM(trans_count), 0) as total_transactions,
                COALESCE(AVG(trans_amount/NULLIF(trans_count, 0)), 0) as avg_transaction_value,
                COUNT(DISTINCT state) as active_states
            FROM aggr_transaction
            {where_clause}
        """
        
        # Users - Use COALESCE to handle NULL
        user_query = f"""
            SELECT 
                COALESCE(SUM(registered_user), 0) as total_users,
                COALESCE(SUM(app_opens), 0) as total_app_opens,
                COALESCE(AVG(app_opens/NULLIF(registered_user, 0)), 0) as avg_engagement
            FROM aggr_user
            {where_clause}
        """
        
        # Insurance - Use COALESCE to handle NULL
        ins_query = f"""
            SELECT 
                COALESCE(SUM(insurance_amount), 0) as total_insurance_amount,
                COALESCE(SUM(insurance_count), 0) as total_policies
            FROM aggr_insurance
            {where_clause}
        """
        
        trans_df = pd.read_sql(trans_query, self.engine, params=params_tuple)
        user_df = pd.read_sql(user_query, self.engine, params=params_tuple)
        ins_df = pd.read_sql(ins_query, self.engine, params=params_tuple)
        
        # Combine all metrics
        summary = {
            **trans_df.to_dict('records')[0],
            **user_df.to_dict('records')[0],
            **ins_df.to_dict('records')[0]
        }
        
        return pd.DataFrame([summary])

    # ============ TRANSACTION ANALYTICS ============
    
    def get_top_states_by_transaction_amount(self, year=None, quarter=None, limit=10):
        """Get top states by transaction amount"""
        query = """
            SELECT state, SUM(trans_amount) as trans_amount, SUM(trans_count) as trans_count
            FROM aggr_transaction
        """
        filters = []
        params = []
        
        if year:
            filters.append("year = %s")
            params.append(year)
        if quarter:
            filters.append("quarter = %s")
            params.append(quarter)
        
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        query += f" GROUP BY state ORDER BY trans_amount DESC LIMIT {limit}"
        
        return pd.read_sql(query, self.engine, params=tuple(params) if params else None)
    
    def get_transaction_type_distribution(self, year=None, quarter=None):
        """Get distribution of transaction types"""
        query = """
            SELECT trans_type, 
                   SUM(trans_amount) as trans_amount, 
                   SUM(trans_count) as trans_count,
                   AVG(trans_amount/trans_count) as avg_transaction_value
            FROM aggr_transaction
        """
        filters = []
        params = []
        
        if year:
            filters.append("year = %s")
            params.append(year)
        if quarter:
            filters.append("quarter = %s")
            params.append(quarter)
        
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        query += " GROUP BY trans_type ORDER BY trans_amount DESC"
        
        return pd.read_sql(query, self.engine, params=tuple(params) if params else None)
    
    def get_quarterly_trends(self, year):
        """Get quarterly transaction trends for a specific year"""
        query = """
            SELECT 
                quarter,
                SUM(trans_amount) as trans_amount,
                SUM(trans_count) as trans_count,
                COUNT(DISTINCT state) as active_states
            FROM aggr_transaction
            WHERE year = %s
            GROUP BY quarter
            ORDER BY quarter
        """
        
        return pd.read_sql(query, self.engine, params=(year,))

    def get_top_districts_by_transaction(self, state=None, year=None, limit=10):
        """Get top districts by transaction amount"""
        query = """
            SELECT 
                state,
                district,
                SUM(trans_amount) as trans_amount,
                SUM(trans_count) as trans_count
            FROM map_transaction
        """
        filters = []
        params = []
        
        if state:
            filters.append("state = %s")
            params.append(state)
        if year:
            filters.append("year = %s")
            params.append(year)
        
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        query += f" GROUP BY state, district ORDER BY trans_amount DESC LIMIT {limit}"
        
        return pd.read_sql(query, self.engine, params=tuple(params) if params else None)

    # ============ USER ANALYTICS ============
    
    def get_user_engagement_metrics(self, year=None, quarter=None):
        """Get user engagement metrics"""
        query = """
            SELECT 
                state,
                SUM(registered_user) as total_users,
                SUM(app_opens) as total_app_opens,
                AVG(app_opens/registered_user) as avg_opens_per_user
            FROM aggr_user
        """
        filters = []
        params = []
        
        if year:
            filters.append("year = %s")
            params.append(year)
        if quarter:
            filters.append("quarter = %s")
            params.append(quarter)
        
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        query += " GROUP BY state ORDER BY total_users DESC"
        
        return pd.read_sql(query, self.engine, params=tuple(params) if params else None)

    def get_device_brand_popularity(self, year=None):
        """Get most popular device brands"""
        query = """
            SELECT 
                device_brand,
                SUM(device_count) as total_devices,
                AVG(device_percentage) as avg_percentage
            FROM aggr_user
        """
        filters = ["device_brand != ''"]
        params = []
        
        if year:
            filters.append("year = %s")
            params.append(year)
        
        query += " WHERE " + " AND ".join(filters)
        query += " GROUP BY device_brand ORDER BY total_devices DESC LIMIT 15"
        
        return pd.read_sql(query, self.engine, params=tuple(params) if params else None)
    
    def get_user_growth_rate(self):
        """Calculate user growth rate over years"""
        query = """
            SELECT 
                year,
                quarter,
                SUM(registered_user) as total_users,
                SUM(app_opens) as total_app_opens
            FROM aggr_user
            GROUP BY year, quarter
            ORDER BY year, quarter
        """
        
        return pd.read_sql(query, self.engine)

    # ============ INSURANCE ANALYTICS ============
    
    def get_insurance_adoption_by_state(self, year=None, quarter=None):
        """Get insurance adoption metrics by state"""
        query = """
            SELECT 
                state,
                SUM(insurance_amount) as insur_amount,
                SUM(insurance_count) as total_policies,
                AVG(insurance_amount/insurance_count) as avg_policy_value
            FROM aggr_insurance
        """
        filters = []
        params = []
        
        if year:
            filters.append("year = %s")
            params.append(year)
        if quarter:
            filters.append("quarter = %s")
            params.append(quarter)
        
        if filters:
            query += " WHERE " + " AND ".join(filters)
        
        query += " GROUP BY state ORDER BY insur_amount DESC"
        
        return pd.read_sql(query, self.engine, params=tuple(params) if params else None)

    # ============ INSIGHTS ANALYTICS ============

    def get_year_over_year_growth(self):
        """Calculate year-over-year transaction growth"""
        query = """
            SELECT 
                year,
                SUM(trans_amount) as trans_amount,
                SUM(trans_count) as trans_count,
                LAG(SUM(trans_amount)) OVER (ORDER BY year) as prev_year_amount,
                LAG(SUM(trans_count)) OVER (ORDER BY year) as prev_year_count
            FROM aggr_transaction
            GROUP BY year
            ORDER BY year
        """
        
        df = pd.read_sql(query, self.engine)
        
        # Calculate growth percentage
        df['amount_growth'] = ((df['trans_amount'] - df['prev_year_amount']) / df['prev_year_amount'] * 100).round(2)
        df['count_growth'] = ((df['trans_count'] - df['prev_year_count']) / df['prev_year_count'] * 100).round(2)
        
        return df

