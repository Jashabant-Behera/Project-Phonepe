import plotly.express as px
import plotly.graph_objects as go

# State name mapping (same as before)
STATE_MAPPING = {
    'andaman-&-nicobar-islands': 'Andaman & Nicobar',
    'andhra-pradesh': 'Andhra Pradesh',
    'arunachal-pradesh': 'Arunachal Pradesh',
    'assam': 'Assam',
    'bihar': 'Bihar',
    'chandigarh': 'Chandigarh',
    'chhattisgarh': 'Chhattisgarh',
    'dadra-&-nagar-haveli-&-daman-&-diu': 'Dadra and Nagar Haveli and Daman and Diu',
    'delhi': 'Delhi',
    'goa': 'Goa',
    'gujarat': 'Gujarat',
    'haryana': 'Haryana',
    'himachal-pradesh': 'Himachal Pradesh',
    'jammu-&-kashmir': 'Jammu & Kashmir',
    'jharkhand': 'Jharkhand',
    'karnataka': 'Karnataka',
    'kerala': 'Kerala',
    'ladakh': 'Ladakh',
    'lakshadweep': 'Lakshadweep',
    'madhya-pradesh': 'Madhya Pradesh',
    'maharashtra': 'Maharashtra',
    'manipur': 'Manipur',
    'meghalaya': 'Meghalaya',
    'mizoram': 'Mizoram',
    'nagaland': 'Nagaland',
    'odisha': 'Odisha',
    'puducherry': 'Puducherry',
    'punjab': 'Punjab',
    'rajasthan': 'Rajasthan',
    'sikkim': 'Sikkim',
    'tamil-nadu': 'Tamil Nadu',
    'telangana': 'Telangana',
    'tripura': 'Tripura',
    'uttar-pradesh': 'Uttar Pradesh',
    'uttarakhand': 'Uttarakhand',
    'west-bengal': 'West Bengal'
}

def map_state_names(df):
    """Map state names to proper format"""
    if 'state' in df.columns:
        df['state'] = df['state'].map(STATE_MAPPING).fillna(df['state'])
    return df

# ============ INDIA MAPS ============

def plot_india_choropleth(df, value_col, title, color_scale='Viridis'):
    """Create India map with state-wise data"""
    df = map_state_names(df.copy())
    
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color=value_col,
        title=title,
        color_continuous_scale=color_scale,
        hover_data=[value_col]
    )
    
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        plot_bgcolor='rgba(26, 26, 26, 0.5)',
        paper_bgcolor='rgba(10, 10, 10, 0.3)',
        font=dict(color='white'),
        title_font_size=20,
        height=850
    )
    
    return fig

def plot_india_heatmap(heatmap_data, metric_name, metric_unit, year, quarter, data_level):
    """Plot heatmap of India with given metric"""
    heatmap_data = map_state_names(heatmap_data.copy())
    
    fig = px.choropleth(
        heatmap_data,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='value',
        hover_name='state',
        hover_data={'value':':.2f', 'state':False},
        color_continuous_scale='Purples',
        labels={'value': metric_name}
    )
    
    fig.update_geos(
        fitbounds="locations",
        visible=False,
        showcountries=False,
        showsubunits=False,
        showland=False
        )
    
    fig.update_layout(
        title={
            'text': f'{metric_name} - {data_level}<br><sub>Year: {year} | Quarter: Q{quarter}</sub>',
            'font': {'size': 20},
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.95,
            'yanchor': 'top'
        },
        plot_bgcolor='rgba(10, 20, 30, 0.7)',
        paper_bgcolor='rgba(0,0,0,0.5)',
        font=dict(color='white'),
        title_font_size=18,
        height=600,
        margin=dict(l=0, r=0, t=80, b=0),
        coloraxis_colorbar=dict(
            title=metric_name,
            thickness=15,
            len=0.7,
            bgcolor='rgba(0,0,0,0)',
            tickfont=dict(color='white')
        )
    )
    
    return fig

# ============ TRANSACTION VISUALIZATIONS ============

def plot_top_states_bar(df, top_n=10):
    """Plot top N states by transaction amount"""
    df = map_state_names(df.copy())
    grouped = df.groupby('state', as_index=False)['trans_amount'].sum()
    grouped = grouped.nlargest(top_n, 'trans_amount')
    grouped['trans_amount'] = grouped['trans_amount'] / 10000000
    
    fig = px.bar(
        grouped,
        x='trans_amount',
        y='state',
        orientation='h',
        title=f'Top {top_n} States by Transaction Amount',
        labels={'trans_amount': 'Amount (Cr)', 'state': 'State'},
        color='trans_amount',
        color_continuous_scale='Purples'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(26, 26, 26, 0.5)',
        paper_bgcolor='rgba(10, 10, 10, 0.3)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#333', showgrid=True),
        yaxis=dict(gridcolor='#333', showgrid=True),
        # Add subtle border
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    return fig

def plot_transaction_type_distribution(df):
    """Plot transaction type distribution as pie chart"""
    grouped = df.groupby('trans_type', as_index=False)['trans_amount'].sum()
    
    fig = px.pie(
        grouped,
        values='trans_amount',
        names='trans_type',
        title='Transaction Distribution by Type',
        color_discrete_sequence=px.colors.sequential.Purples_r
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(26, 26, 26, 0.5)',
        paper_bgcolor='rgba(10, 10, 10, 0.3)',
        font=dict(color='white')
    )
    
    return fig

def plot_quarterly_comparison(df):
    """Compare quarters within a year"""
    if 'quarter' not in df.columns:
        return None
    
    grouped = df.groupby('quarter', as_index=False).agg({
        'trans_amount': 'sum',
        'trans_count': 'sum'
    })
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=grouped['quarter'],
        y=grouped['trans_amount'] / 10000000,
        name='Amount (Cr)',
        marker_color='#667eea'
    ))
    
    fig.update_layout(
        title='Quarterly Performance',
        xaxis_title='Quarter',
        yaxis_title='Transaction Amount (Cr)',
        plot_bgcolor='rgba(26, 26, 26, 0.5)',
        paper_bgcolor='rgba(10, 10, 10, 0.3)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#333'),
        yaxis=dict(gridcolor='#333')
    )
    
    return fig

def plot_top_districts_bar(df,selected_state="", top_n=10):

    df_plot = df.nlargest(top_n, 'trans_amount') 

    fig = px.bar(
        df_plot,
        x='trans_amount',
        y='district',
        orientation='h',
        title = f'Top {top_n} Districts in {selected_state}',
        labels={'trans_amount':'Transaction Amount', 'district':'District'},
        color='trans_amount',
        color_continuous_scale='Purples'
    )

    fig.update_layout(
        plot_bgcolor='rgba(26, 26, 26, 0.5)',
        paper_bgcolor='rgba(10, 10, 10, 0.3)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', showgrid=True),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', showgrid=True),
        title=dict(font=dict(size=18, color='#667eea'))
    )

    return fig

# ============ USER VISUALIZATIONS ============

def plot_user_engagement(df):
    """Plot user engagement metrics"""
    df = map_state_names(df.copy())
    grouped = df.groupby('state', as_index=False).agg({
        'total_users': 'sum',
        'total_app_opens': 'sum'
    })
    
    grouped['engagement_rate'] = (grouped['total_app_opens'] / grouped['total_users']).round(2)
    grouped = grouped.nlargest(15, 'engagement_rate')
    
    fig = px.bar(
        grouped,
        x='state',
        y='engagement_rate',
        title='User Engagement Rate by State (App Opens per User)',
        labels={'engagement_rate': 'Engagement Rate', 'state': 'State'},
        color='engagement_rate',
        color_continuous_scale='Purples'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(26, 26, 26, 0.5)',
        paper_bgcolor='rgba(10, 10, 10, 0.3)',
        font=dict(color='white'),
        xaxis_tickangle=-45,
        xaxis=dict(gridcolor='#333'),
        yaxis=dict(gridcolor='#333')
    )
    
    return fig

def plot_device_brands(df):
    """Plot device brand distribution"""
    if 'device_brand' not in df.columns:
        return None
    
    grouped = df.groupby('device_brand', as_index=False)['total_devices'].sum()
    grouped = grouped[grouped['device_brand'] != '']
    grouped = grouped.nlargest(10, 'total_devices')
    
    fig = px.bar(
        grouped,
        x='device_brand',
        y='total_devices',
        title='Top Device Brands',
        labels={'total_devices': 'Device Count', 'device_brand': 'Brand'},
        color='total_devices',
        color_continuous_scale='Purples'
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(26, 26, 26, 0.5)',
        paper_bgcolor='rgba(10, 10, 10, 0.3)',
        font=dict(color='white'),
        xaxis_tickangle=-45,
        xaxis=dict(gridcolor='#333'),
        yaxis=dict(gridcolor='#333')
    )
    
    return fig

def plot_user_growth(df):
    """Plot user growth over time"""
    if 'year' not in df.columns or 'quarter' not in df.columns:
        return None
    
    df['period'] = df['year'].astype(str) + '-Q' + df['quarter'].astype(str)
    grouped = df.groupby('period', as_index=False)['total_users'].sum()
    grouped['total_users'] = grouped['total_users'] / 10000000
    
    fig = px.line(
        grouped,
        x='period',
        y='total_users',
        title='Registered User Growth Over Time',
        labels={'total_users': 'Users (Cr)', 'period': 'Period'},
        markers=True
    )
    
    fig.update_traces(line=dict(color='#667eea', width=3), marker=dict(size=10))
    
    fig.update_layout(
        plot_bgcolor='rgba(26, 26, 26, 0.5)',
        paper_bgcolor='rgba(10, 10, 10, 0.3)',
        font=dict(color='white'),
        xaxis=dict(gridcolor='#333'),
        yaxis=dict(gridcolor='#333')
    )
    
    return fig

# ============ INSURANCE VISUALIZATIONS ============

def plot_insurance_map(df):
    """Plot insurance data on India map"""
    df = map_state_names(df.copy())
    grouped = df.groupby('state', as_index=False)['insur_amount'].sum()
    
    return plot_india_choropleth(
        grouped,
        'insur_amount',
        'Insurance Amount by State',
        'Purples'
    )
