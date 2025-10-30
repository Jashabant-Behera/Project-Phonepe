import streamlit as st
import pandas as pd
from src.sql.sql_queries import *
from src.sql.sql_analysis import PhonePeAnalytics
from src.visualization import *

st.set_page_config(
    page_title="Project PhonePe Pulse",
    page_icon="./src/icons/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling - Clean Black Theme
st.markdown("""
    <style>
        /* Root variables for easy theme customization */
        :root{
            /* Backgrounds & cards */
            --bg: #0b0b0d;              /* page background */
            --panel: rgba(20,20,24,0.78); /* frosted panel bg */
            --card: #111115;            /* card solid fallback */
            --glass-border: rgba(255,255,255,0.04);

            /* Accent colors (gradient start/end) */
            --accent-1: #7b61ff;
            --accent-2: #9d8eff;

            /* Text */
            --text-primary: #e7e7eb;
            --text-muted: #9aa0a6;

            /* Borders / subtle lines */
            # --line: rgba(255,255,255,0.04);

            --radius-lg: 14px;
            --radius-md: 10px;
            --radius-sm: 8px;

            --ease: cubic-bezier(.2,.9,.3,1);
            --card-shadow: 0 8px 30px rgba(2,6,23,0.6);
            --soft-shadow: 0 6px 18px rgba(2,6,23,0.45);
        }

        /* Global page base */
        .stApp, .main {
            background: #2C034A;
            background: radial-gradient(circle, rgba(44, 3, 74, 1) 10%, rgba(44, 3, 74, 1) 20%, rgba(0, 0, 0, 1) 100%);
            color: var(--text-primary);
            font-family: 'Inter', 'Poppins', 'Roboto', system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
            line-height: 1.5;
            transition: background 400ms var(--ease), color 300ms var(--ease);
            padding: 18px 20px 36px 20px; 
        }

        /* Import preferred font (safe: placed here; network required) */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');

        /* ---------------------------
        Container sizing & layout
        --------------------------- */
        .block-container {
            max-width: 1280px;      
            margin: 0 auto;
            padding: 18px;
            box-sizing: border-box;
        }

        /* ---------------------------
        Card & panel base (glassmorphism)
        --------------------------- */
        .card, .dashboard-card, .metric-card, .insight-box {
            background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
            backdrop-filter: blur(6px) saturate(110%);
            -webkit-backdrop-filter: blur(6px) saturate(110%);
            border: 1px solid var(--glass-border);
            border-radius: var(--radius-lg);
            box-shadow: var(--card-shadow);
            padding: 16px;
            transition: transform 300ms var(--ease), box-shadow 300ms var(--ease), border-color 300ms var(--ease);
        }

        /* Lift effect on hover for interactive cards */
        .card:hover, .metric-card:hover, .dashboard-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 18px 45px rgba(2,6,23,0.65);
            border-color: rgba(125,97,255,0.18);
        }

        /* ---------------------------
        Header / Titles
        --------------------------- */
        /* Gradient-accented main title â€” uses background-clip for vibrant headings */
        .main-title {
            font-weight: 800;
            font-size: 2.6rem;
            line-height: 1.02;
            margin: 6px 0 6px;
            letter-spacing: -0.6px;
            background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Subtitles / small descriptions */
        .subtitle {
            color: var(--text-muted);
            margin-bottom: 18px;
            font-size: 0.98rem;
        }

        /* Section headings */
        .section-header {
            font-size: 1.4rem;
            font-weight: 700;
            color: var(--text-primary);
            margin: 14px 0;
            display: inline-block;
            padding-bottom: 8px;
            border-bottom: 2px solid linear-gradient(90deg, transparent, transparent);
        }

        /* Accent underline for section headers (nice touch) */
        .section-header:after{
            content: "";
            display:block;
            height:3px;
            width:64px;
            margin-top:8px;
            border-radius:4px;
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
        }

        /* ---------------------------
        Buttons & Inputs
        --------------------------- */
        /* Primary buttons (Streamlit's rendered button inside .stButton) */
        .stButton>button, button[kind="primary"]{
            background: linear-gradient(135deg, var(--accent-1), var(--accent-2));
            color: white !important;
            border: none;
            padding: 10px 16px;
            font-weight: 700;
            border-radius: 10px;
            box-shadow: 0 8px 22px rgba(125,97,255,0.18);
            transition: transform 220ms var(--ease), box-shadow 220ms var(--ease), opacity 220ms var(--ease);
            cursor: pointer;
        }

        /* Button hover & active */
        .stButton>button:hover, button[kind="primary"]:hover {
            transform: translateY(-3px);
            box-shadow: 0 18px 36px rgba(125,97,255,0.22);
            opacity: 0.98;
        }

        .stButton>button:active, button[kind="primary"]:active {
            transform: translateY(0);
            box-shadow: 0 6px 14px rgba(2,6,23,0.5);
        }

        /* Secondary / ghost style for other controls */
        .stButton>div>button, .stButton>button.secondary {
            background: transparent;
            border: 1px solid rgba(255,255,255,0.06);
            color: var(--text-primary);
        }

        /* Selectboxes / multiselects / text inputs â€” unify input look */
        [data-testid="stSelectbox"], [data-testid="stMultiselect"], .stTextInput, .stNumberInput, .stDateInput {
            border-radius: var(--radius-sm) !important;
            background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.00));
            border: 1px solid var(--line);
            padding: 8px 10px;
            color: var(--text-primary);
            transition: border-color 200ms var(--ease), box-shadow 200ms var(--ease);
        }

        /* Input focus */
        [data-testid="stSelectbox"]:focus-within, [data-testid="stMultiselect"]:focus-within, input:focus, textarea:focus {
            outline: none;
            border-color: rgba(125,97,255,0.36);
            box-shadow: 0 8px 22px rgba(125,97,255,0.08);
        }

        /* Label coloring to tie with accent */
        label, .stSelectbox label, .stMultiSelect label {
            color: var(--text-muted);
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        /* ---------------------------
        Tabs styling (Streamlit uses BaseWeb tabs) 
        --------------------------- */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--line);
            margin-bottom: 18px;
        }

        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: var(--text-muted);
            border-radius: 10px 10px 0 0;
            padding: 8px 14px;
            font-weight: 600;
            transition: all 180ms var(--ease);
            border: 1px solid transparent;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            color: white;
            background: linear-gradient(135deg, rgba(123,97,255,0.12), rgba(157,142,255,0.06));
            border: 1px solid rgba(125,97,255,0.14);
            box-shadow: 0 8px 18px rgba(2,6,23,0.4);
        }

        /* ---------------------------
        Metric cards (your custom .metric-card class)
        --------------------------- */
        .metric-card {
            /* re-use card style but slightly denser */
            background: linear-gradient(180deg, rgba(255,255,255,0.015), rgba(255,255,255,0.008));
            border-radius: 12px;
            padding: 18px;
            text-align: left;
            min-height: 86px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            gap: 6px;
        }

        .metric-label {
            color: var(--text-muted);
            font-size: 0.79rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.9px;
        }

        .metric-value {
            font-size: 1.65rem;
            font-weight: 800;
            line-height: 1;
            background: linear-gradient(90deg, var(--accent-1), var(--accent-2));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        /* Streamlit native metric fallback */
        [data-testid="metric-container"] div[role="listitem"] {
            border-radius: 10px;
        }

        /* ---------------------------
        Tables / Dataframe styling
        - We style both the 'st.dataframe' interactive and the static 'st.table' containers.
        --------------------------- */
        /* Outer wrapper for Streamlit dataframes */
        .stDataFrame, .stTable {
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--glass-border);
            box-shadow: var(--soft-shadow);
        }

        /* Dataframe inner table (works for modern Streamlit versions) */
        .stDataFrame > div[role="grid"], .stTable > div[role="table"] {
            background: transparent;
        }

        /* Header row style */
        .stDataFrame thead th, .stTable table thead th {
            background: linear-gradient(90deg, rgba(123,97,255,0.06), rgba(157,142,255,0.02));
            color: var(--text-primary);
            font-weight: 700;
            padding: 10px 12px;
            border-bottom: 1px solid rgba(255,255,255,0.03);
            text-align: left;
        }

        /* Body rows */
        .stDataFrame tbody tr, .stTable table tbody tr {
            background: linear-gradient(180deg, rgba(255,255,255,0.003), rgba(255,255,255,0.001));
            color: var(--text-primary);
        }

        /* Row hover highlight */
        .stDataFrame tbody tr:hover, .stTable table tbody tr:hover {
            background: linear-gradient(90deg, rgba(123,97,255,0.04), rgba(123,97,255,0.02));
            transform: translateY(-1px);
        }

        /* Cell padding & font */
        .stDataFrame td, .stTable table td {
            padding: 10px 12px;
            font-size: 0.95rem;
            color: var(--text-primary);
        }

        /* Small responsive table tweak: horizontal scroll container */
        .stDataFrame > div[role="grid"] > div[role="row"] {
            -webkit-overflow-scrolling: touch;
        }

        /* ---------------------------
        Plotly / chart card styling hint
        - apply wrapping class 'card' to chart containers in your app
        --------------------------- */
        .stPlotlyChart, .element-container .plotly {
            border-radius: 12px;
            padding: 8px;
        }

        /* If you wrap charts in a div.card the background will be consistent */
        .card .stPlotlyChart, .card .streamlit-plotly-chart {
            padding: 12px;
            background: transparent;
        }

        /* ---------------------------
        Sidebar (polished)
        --------------------------- */
        .sidebar .css-1lcbmhc { /* generic wrapper â€” class names may vary - keep minimal */
            background: linear-gradient(180deg, rgba(255,255,255,0.01), rgba(255,255,255,0.005));
            border-radius: 12px;
            padding: 14px;
            border: 1px solid var(--glass-border);
            box-shadow: var(--soft-shadow);
        }

        /* Sidebar headings */
        .sidebar h3 {
            color: var(--text-primary);
            font-weight: 700;
        }

        /* ---------------------------
        Insight box (used in your app)
        --------------------------- */
        .insight-box {
            border-left: 4px solid transparent;
            border-image: linear-gradient(180deg, var(--accent-1), var(--accent-2)) 1;
            padding: 14px;
            margin: 12px 0;
            border-radius: var(--radius-lg);
        }

        /* Insight title & text */
        .insight-title { color: var(--accent-1); font-weight: 700; margin-bottom: 6px; }
        .insight-text { color: var(--text-muted); line-height: 1.6; font-size: 0.96rem; }

        /* ---------------------------
        Small UI niceties
        --------------------------- */
        /* Hide Streamlit's header, menu, and footer for a clean full-screen presentation */
        header, #MainMenu, footer, .reportview-container .main footer {
            # visibility: hidden;
            # height: 0;
        }

        /* Tiny helper: subtle dividing lines for layout clarity */
        .row-divider { height: 1px; background: var(--line); margin: 18px 0; border-radius: 2px; }

        /* ---------------------------
        Scrollbar (WebKit browsers)
        --------------------------- */
        ::-webkit-scrollbar { width: 10px; height: 10px; }
        ::-webkit-scrollbar-thumb {
            border-radius: 999px;
            background: linear-gradient(180deg, var(--accent-1), var(--accent-2));
            box-shadow: inset 0 0 4px rgba(0,0,0,0.35);
        }
        ::-webkit-scrollbar-track { background: rgba(255,255,255,0.01); border-radius: 8px; }

        /* ---------------------------
        Responsive typography & spacing
        --------------------------- */
        @media (max-width: 1024px){
            .main-title { font-size: 2.2rem; }
            .metric-value { font-size: 1.4rem; }
            .block-container { padding: 12px; }
        }

        @media (max-width: 600px){
            .main-title { font-size: 1.6rem; }
            .section-header { font-size: 1.05rem; }
            .card, .metric-card { padding: 12px; border-radius: 10px; }
            .block-container { padding-left: 10px; padding-right: 10px; }
        }

        /* ---------------------------
        Accessibility / small contrast improvements
        --------------------------- */
        /* Make focus outlines more visible */
        :focus { outline: 3px solid rgba(125,97,255,0.18); outline-offset: 2px; }
    </style>
""", unsafe_allow_html=True)

# Initialize analytics
analytics = PhonePeAnalytics()

st.markdown("<br>", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-title">Project PhonePe Pulse</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Explore India\'s Digital Payment Trends -  Powered by Data Analytics</p>', unsafe_allow_html=True)

# Sidebar filters

st.markdown("### Filters")
col1, col2 = st.columns(2)

with col1:
    year_options = ["All", 2018, 2019, 2020, 2021, 2022]
    selected_year = st.selectbox(" Select Year", year_options, index=len(year_options)-1)

with col2:
    quarter_options = ["All", 1, 2, 3, 4]
    selected_quarter = st.selectbox(" Select Quarter", quarter_options)
    

# Parse filters
year_val = None if selected_year == "All" else selected_year
quarter_val = None if selected_quarter == "All" else selected_quarter


# Main tabs
tabs = st.tabs([
    "Overview",
    "Transactions",
    "Users",
    "Insurance",
    "Raw Data",
    "Insights"
])

# ==================== OVERVIEW TAB ====================
with tabs[0]:
    st.markdown('<h2 class="section-header">Executive Summary</h2>', unsafe_allow_html=True)
    
    # Get executive summary
    summary_df = analytics.get_executive_summary(year_val, quarter_val)
    
    if not summary_df.empty:
        summary = summary_df.iloc[0]

        def safe_divide(value, divisor=10000000):
            return (value / divisor) if value is not None else 0
            
        # Top metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            trans_amount = safe_divide(summary.get('total_transaction_amount'))
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Transaction Amount</div>
                    <div class="metric-value">₹ {trans_amount:.2f} Cr</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            trans_count = safe_divide(summary.get('total_transactions'))
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Total Transactions</div>
                    <div class="metric-value">₹ {trans_count:.2f} Cr</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            total_users = safe_divide(summary.get('total_users'))
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Registered Users</div>
                    <div class="metric-value">{total_users:.2f} Cr</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            avg_trans = summary['avg_transaction_value']
            avg_trans = avg_trans if avg_trans is not None else 0
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Avg Transaction</div>
                    <div class="metric-value">₹ {avg_trans:.2f}</div>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown(" ")
        
        # Second row metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            app_opens = safe_divide(summary.get('total_app_opens'))
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">App Opens</div>
                    <div class="metric-value">{app_opens:.2f} Cr</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            insurance_amt = safe_divide(summary.get('total_insurance_amount'))

            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Insurance Amount</div>
                    <div class="metric-value">₹ {insurance_amt:.2f} Cr</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            policies = safe_divide(summary.get('total_policies'))
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Insurance Policies</div>
                    <div class="metric-value">{policies:.2f} Cr</div>
                </div>
            ''', unsafe_allow_html=True)
    
    else:
        st.warning("No data available for the selected year and quarter.")

    
    st.markdown("<br>", unsafe_allow_html=True)

    # Top performing states
    st.markdown("### Top Performing States")
    st.markdown('<p class="subtitle">Top 10 Aggregated Transaction Table</p>', unsafe_allow_html=True)
    top_states_df = analytics.get_top_states_by_transaction_amount(year_val, quarter_val, limit=10)
    
    col1, col2 = st.columns([2, 1])
    
    if not top_states_df.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = plot_top_states_bar(top_states_df, top_n=10)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(
                top_states_df[['state', 'trans_amount', 'trans_count']].head(10),
                use_container_width=True,
                height=400
            )
    else:
        st.info("No transaction data available for the selected period.")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # ============ INDIA GEOGRAPHIC HEATMAP ============

    st.markdown('<h2 class="section-header">India Geographic Heatmap</h2>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Explore state-wise, district-wise, or pincode-wise metrics on an interactive map</p>', unsafe_allow_html=True)
    
    # Independent filters for heatmap
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        heatmap_year_options = [2018, 2019, 2020, 2021, 2022]
        heatmap_year = st.selectbox("Year", heatmap_year_options, index=len(heatmap_year_options)-1, key="heatmap_year")
    
    with col2:
        heatmap_quarter_options = [1, 2, 3, 4]
        heatmap_quarter = st.selectbox("Quarter", heatmap_quarter_options, index=0, key="heatmap_quarter")
    
    with col3:
        heatmap_data_type = st.selectbox("Data Type", ["Transactions", "Users", "Insurance"], key="heatmap_data_type")
    
    with col4:
        # Category options based on data type
        if heatmap_data_type == "Transactions":
            category_options = ["All Categories", "Recharge & bill payments", "Peer-to-peer payments", "Merchant payments", "Financial Services", "Others"]
        else:
            category_options = ["All Categories"]
        
        heatmap_category = st.selectbox("Category", category_options, key="heatmap_category")
    
    with col5:
        heatmap_data_level = st.selectbox("Level", ["State", "District", "Pincode"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Fetch data based on filters
    try:
        if heatmap_data_level == "State":
            if heatmap_data_type == "Transactions":
                heatmap_df = get_aggr_transaction(heatmap_year, heatmap_quarter)
                if not heatmap_df.empty:
                    if heatmap_category != "All Categories":
                        heatmap_df = heatmap_df[heatmap_df['trans_type'] == heatmap_category]
                    
                    heatmap_data = heatmap_df.groupby('state', as_index=False).agg({
                        'trans_amount': 'sum',
                        'trans_count': 'sum'
                    })
                    heatmap_data.rename(columns={'trans_amount': 'value', 'trans_count': 'count'}, inplace=True)
                    metric_name = "Transaction Amount"
                    metric_unit = "₹ Cr"
                    count_label = "Transactions"
                
            elif heatmap_data_type == "Users":
                heatmap_df = get_aggr_user(heatmap_year, heatmap_quarter)
                if not heatmap_df.empty:
                    heatmap_data = heatmap_df.groupby('state', as_index=False).agg({
                        'registered_user': 'sum',
                        'app_opens': 'sum'
                    })
                    heatmap_data.rename(columns={'registered_user': 'value', 'app_opens': 'count'}, inplace=True)
                    metric_name = "Registered Users"
                    metric_unit = "Cr"
                    count_label = "App Opens"
            
            else:  # Insurance
                heatmap_df = get_aggr_insurance(heatmap_year, heatmap_quarter)
                if not heatmap_df.empty:
                    if heatmap_category != "All Categories":
                        heatmap_df = heatmap_df[heatmap_df['insurance_type'] == heatmap_category]
                    
                    heatmap_data = heatmap_df.groupby('state', as_index=False).agg({
                        'insurance_amount': 'sum',
                        'insurance_count': 'sum'
                    })
                    heatmap_data.rename(columns={'insurance_amount': 'value', 'insurance_count': 'count'}, inplace=True)
                    metric_name = "Insurance Amount"
                    metric_unit = "₹ Cr"
                    count_label = "Policies"
        
        elif heatmap_data_level == "District":
            # Use map data for district level
            if heatmap_data_type == "Transactions":
                heatmap_df = get_map_transaction(heatmap_year, heatmap_quarter)
                if not heatmap_df.empty:
                    if heatmap_category != "All Categories":
                        heatmap_df = heatmap_df[heatmap_df['trans_type'] == heatmap_category]
                    
                    heatmap_data = heatmap_df.groupby('state', as_index=False).agg({
                        'trans_amount': 'sum',
                        'trans_count': 'sum'
                    })
                    heatmap_data.rename(columns={'trans_amount': 'value', 'trans_count': 'count'}, inplace=True)
                    metric_name = "Transaction Amount"
                    metric_unit = "₹ Cr"
                    count_label = "Transactions"
            
            elif heatmap_data_type == "Users":
                heatmap_df = get_map_user(heatmap_year, heatmap_quarter)
                if not heatmap_df.empty:
                    heatmap_data = heatmap_df.groupby('state', as_index=False).agg({
                        'registered_user': 'sum',
                        'app_opens': 'sum'
                    })
                    heatmap_data.rename(columns={'registered_user': 'value', 'app_opens': 'count'}, inplace=True)
                    metric_name = "Registered Users"
                    metric_unit = "Cr"
                    count_label = "App Opens"
            
            else:  # Insurance
                heatmap_df = get_map_insurance(heatmap_year, heatmap_quarter)
                if not heatmap_df.empty:
                    if heatmap_category != "All Categories":
                        heatmap_df = heatmap_df[heatmap_df['insurance_type'] == heatmap_category]
                    
                    heatmap_data = heatmap_df.groupby('state', as_index=False).agg({
                        'insurance_amount': 'sum',
                        'insurance_count': 'sum'
                    })
                    heatmap_data.rename(columns={'insurance_amount': 'value', 'insurance_count': 'count'}, inplace=True)
                    metric_name = "Insurance Amount"
                    metric_unit = "₹ Cr"
                    count_label = "Policies"
        
        else:  # Pincode level
            # Use top data for pincode level, aggregate to state
            if heatmap_data_type == "Transactions":
                heatmap_df = analytics.get_top_transaction_pincode_wise_data(heatmap_year, heatmap_quarter)
                if not heatmap_df.empty:
                    if heatmap_category != "All Categories":
                        heatmap_df = heatmap_df[heatmap_df['trans_type'] == heatmap_category]
                    
                    heatmap_data = heatmap_df.groupby('state', as_index=False).agg({
                        'total_trans_amount': 'sum',
                        'total_trans_count': 'sum'
                    })
                    heatmap_data.rename(columns={'total_trans_amount': 'value', 'total_trans_count': 'count'}, inplace=True)
                    metric_name = "Transaction Amount"
                    metric_unit = "₹ Cr"
                    count_label = "Transactions"
            
            elif heatmap_data_type == "Users":
                heatmap_df = analytics.get_top_user_pincode_wise_data(heatmap_year, heatmap_quarter)
                if not heatmap_df.empty:
                    heatmap_data = heatmap_df.groupby('state', as_index=False).agg({
                        'total_registered_users': 'sum'
                    })
                    heatmap_data.rename(columns={'total_registered_users': 'value'}, inplace=True)
                    heatmap_data['count'] = 0  # No count for users at pincode level
                    metric_name = "Registered Users"
                    metric_unit = "Cr"
                    count_label = "Users"
            
            else:  # Insurance
                heatmap_df = analytics.get_top_insurance_pincode_wise_data(heatmap_year, heatmap_quarter)
                if not heatmap_df.empty:
                    if heatmap_category != "All Categories":
                        heatmap_df = heatmap_df[heatmap_df['insurance_type'] == heatmap_category]
                    
                    heatmap_data = heatmap_df.groupby('state', as_index=False).agg({
                        'total_insurance_amount': 'sum',
                        'total_insurance_count': 'sum'
                    })
                    heatmap_data.rename(columns={'total_insurance_amount': 'value', 'total_insurance_count': 'count'}, inplace=True)
                    metric_name = "Insurance Amount"
                    metric_unit = "₹ Cr"
                    count_label = "Policies"
        
        # Display heatmap and summary cards
        if not heatmap_data.empty:
            # Map state names
            heatmap_data = map_state_names(heatmap_data.copy())
            
            # Calculate summary metrics
            total_value = heatmap_data['value'].sum()
            avg_value = heatmap_data['value'].mean()
            top_state = heatmap_data.loc[heatmap_data['value'].idxmax(), 'state'] if len(heatmap_data) > 0 else "N/A"
            top_state_value = heatmap_data['value'].max() if len(heatmap_data) > 0 else 0
            total_count = heatmap_data['count'].sum() if 'count' in heatmap_data.columns else 0
            num_regions = len(heatmap_data)
            
            # Convert to crores for display
            total_value_cr = total_value / 10000000
            avg_value_cr = avg_value / 10000000
            top_state_value_cr = top_state_value / 10000000
            total_count_cr = total_count / 10000000 if total_count > 10000000 else total_count
            
            # Two-column layout
            col1, col2 = st.columns([2.5, 1])
            
            with col1:
                # Create choropleth map
                fig = plot_india_heatmap(heatmap_data, metric_name, metric_unit, heatmap_year, heatmap_quarter, heatmap_data_level)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Summary Card 1: Total Value
                if metric_unit == "₹ Cr":
                    st.markdown(f'''
                        <div class="metric-card">
                            <div class="metric-label">Total {metric_name}</div>
                            <div class="metric-value">{metric_unit} {total_value_cr:.2f}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                        <div class="metric-card">
                            <div class="metric-label">Total {metric_name}</div>
                            <div class="metric-value">{total_value_cr:.2f} {metric_unit}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Summary Card 2: Average Value
                if metric_unit == "₹ Cr":
                    st.markdown(f'''
                        <div class="metric-card">
                            <div class="metric-label">Average {metric_name}</div>
                            <div class="metric-value">{metric_unit} {avg_value_cr:.2f}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                        <div class="metric-card">
                            <div class="metric-label">Average {metric_name}</div>
                            <div class="metric-value">{avg_value_cr:.2f} {metric_unit}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Summary Card 3: Top State
                st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-label">Top Performing State</div>
                        <div class="metric-value" style="font-size: 1.3rem;">{top_state}</div>
                        <div class="metric-label" style="margin-top: 8px;">{metric_unit} {top_state_value_cr:.2f}</div>
                    </div>
                ''', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                # Summary Card 4: Count metric
                if total_count > 0:
                    count_display = f"{total_count_cr:.2f} Cr" if total_count > 10000000 else f"{total_count:,.0f}"
                    st.markdown(f'''
                        <div class="metric-card">
                            <div class="metric-label">Total {count_label}</div>
                            <div class="metric-value">{count_display}</div>
                        </div>
                    ''', unsafe_allow_html=True)
                else:
                    st.markdown(f'''
                        <div class="metric-card">
                            <div class="metric-label">Active Regions</div>
                            <div class="metric-value">{num_regions}</div>
                        </div>
                    ''', unsafe_allow_html=True)
        
        else:
            st.warning(f"No data available for {heatmap_data_type} at {heatmap_data_level} level for Year {heatmap_year}, Quarter {heatmap_quarter}")
    
    except Exception as e:
        st.error(f"Error loading heatmap data or Data is not present in the database")
        st.info("Please check your data filters and try again.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    

# ==================== TRANSACTIONS TAB ====================
with tabs[1]:
    st.markdown('<h2 class="section-header">Transaction Analytics</h2>', unsafe_allow_html=True)
    
    # Transaction type distribution
    st.markdown("### Transaction Type Distribution")
    st.markdown('<p class="subtitle">Aggregated Transaction Distribution</p>', unsafe_allow_html=True)
    trans_type_df = analytics.get_transaction_type_distribution(year_val, quarter_val)
    
    if not trans_type_df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = plot_transaction_type_distribution(trans_type_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            st.dataframe(trans_type_df, use_container_width=True, height=400)
    
    # Quarterly trends
    if year_val:
        st.markdown("### Quarterly Trends")
        st.markdown('<p class="subtitle">Quarterly Aggregated Transaction</p>', unsafe_allow_html=True)
        quarterly_df = analytics.get_quarterly_trends(year_val)
        
        if not quarterly_df.empty:
            fig = plot_quarterly_comparison(quarterly_df)
            st.plotly_chart(fig, use_container_width=True)
    
    # State-wise map
    st.markdown("### State-wise Transaction Map")
    top_states = analytics.get_top_states_by_transaction_amount(year_val, quarter_val, limit=50)
    
    if not top_states.empty:
        top_states.rename(columns={'trans_amount': 'trans_amount'}, inplace=True)
        fig = plot_india_choropleth(top_states, 'trans_amount', 'Transaction Amount by State', 'Purples')
        st.plotly_chart(fig, use_container_width=True)
    
    # Top districts
    st.markdown("### Top Districts")
    st.markdown('<p class="subtitle">Top Districts from Map Transaction</p>', unsafe_allow_html=True)
    selected_state = st.selectbox("Select State for District Analysis", 
                                   ["All"] + list(top_states['state'].unique()) if not top_states.empty else ["All"])
    
    if selected_state != "All":
        district_df = analytics.get_top_districts_by_transaction(
            selected_state.lower().replace(' ', '-').replace('&', '&'),
            year_val,
            limit=10
        )
        
        if not district_df.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                fig = plot_top_districts_bar(district_df, selected_state, top_n=10)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                st.dataframe(district_df, use_container_width=True, height=400)

# ==================== USERS TAB ====================
with tabs[2]:
    st.markdown('<h2 class="section-header">User Analytics</h2>', unsafe_allow_html=True)
    
    # User engagement metrics
    st.markdown("### User Engagement")
    st.markdown('<p class="subtitle">Aggeregated User Engagement</p>', unsafe_allow_html=True)
    engagement_df = analytics.get_user_engagement_metrics(year_val, quarter_val)
    
    if not engagement_df.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_users = engagement_df['total_users'].sum() / 10000000 if engagement_df['total_users'].sum() else 0
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Total Users</div>
                    <div class="metric-value">{total_users:.2f}Cr</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            total_opens = engagement_df['total_app_opens'].sum() / 10000000 if engagement_df['total_app_opens'].sum() else 0
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">App Opens</div>
                    <div class="metric-value">{total_opens:.2f}Cr</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            avg_engagement = engagement_df['avg_opens_per_user'].mean() if not engagement_df['avg_opens_per_user'].isna().all() else 0
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Avg Engagement</div>
                    <div class="metric-value">{avg_engagement:.1f}x</div>
                </div>
            ''', unsafe_allow_html=True)
        
        # Engagement chart
        fig = plot_user_engagement(engagement_df)
        st.plotly_chart(fig, use_container_width=True)
    
    # Device brands
    st.markdown("### Device Brand Analysis")
    st.markdown('<p class="subtitle">Aggeregated User Devices</p>', unsafe_allow_html=True)
    device_df = analytics.get_device_brand_popularity(year_val)
    
    if not device_df.empty:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = plot_device_brands(device_df)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.dataframe(device_df, use_container_width=True, height=400)
    
    # User growth
    st.markdown("### User Growth Trend")
    st.markdown('<p class="subtitle">Aggeregated User Growth</p>', unsafe_allow_html=True)
    growth_df = analytics.get_user_growth_rate()
    
    if not growth_df.empty:
        fig = plot_user_growth(growth_df)
        st.plotly_chart(fig, use_container_width=True)

# ==================== INSURANCE TAB ====================
with tabs[3]:
    st.markdown('<h2 class="section-header">Insurance Analytics</h2>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Aggeregated Insurance Adoption</p>', unsafe_allow_html=True)
    
    # Insurance metrics
    insurance_df = analytics.get_insurance_adoption_by_state(year_val, quarter_val)
    
    if not insurance_df.empty:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_ins = insurance_df['insur_amount'].sum() / 10000000
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Insurance Amount</div>
                    <div class="metric-value">₹ {total_ins:.2f}Cr</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            total_policies = insurance_df['total_policies'].sum() / 10000000
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Total Policies</div>
                    <div class="metric-value">{total_policies:.2f}Cr</div>
                </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            avg_policy = insurance_df['avg_policy_value'].mean()
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Avg Policy Value</div>
                    <div class="metric-value">₹ {avg_policy:.0f}</div>
                </div>
            ''', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Insurance map
        st.markdown("### State-wise Insurance Distribution")
        fig = plot_insurance_map(insurance_df)
        st.plotly_chart(fig, use_container_width=True)
    
# ==================== RAW DATA TAB ====================
with tabs[4]:
    st.markdown('<h2 class="section-header">Raw Data Explorer</h2>', unsafe_allow_html=True)
    
    st.info("Explore raw data from database tables")

    col1, col2, col3 = st.columns(3)

    with col1:
        data_category = st.selectbox(
            "Select Data Category",
            ["Aggregated Data", "Map Level Data", "Top Level Data"]
        )
    
    with col2:
        data_type = st.selectbox(
            "Data Type",
            ["Transactions", "Users", "Insurance"]
        )

    with col3:
        data_level = None
        if data_category == "Top Level Data":

            data_level = st.selectbox(
                "Select Data Level",
                ["Master Data", "District Level", "Pincode Level"]
            )
    
    if data_category == "Aggregated Data":
        if data_type == "Transactions":
            df = get_aggr_transaction(year_val, quarter_val)
            st.markdown("### Aggregated Transaction Data")
        elif data_type == "Users":
            df = get_aggr_user(year_val, quarter_val)
            st.markdown("### Aggregated User Data")
        else:
            df = get_aggr_insurance(year_val, quarter_val)
            st.markdown("### Aggregated Insurance Data")
    
    elif data_category == "Map Level Data":
        if data_type == "Transactions":
            df = get_map_transaction(year_val, quarter_val)
            st.markdown("### Map Transaction Data")
        elif data_type == "Users":
            df = get_map_user(year_val, quarter_val)
            st.markdown("### Map User Data")
        else:
            df = get_map_insurance(year_val, quarter_val)
            st.markdown("### Map Insurance Data")
    
    else:  # Top Level Data
        if data_level == "Master Data":
            if data_type == "Transactions":
                df = get_top_transaction(year_val, quarter_val)
                st.markdown("### Top Transaction Data - Master Level")
            elif data_type == "Users":
                df = get_top_user(year_val, quarter_val)
                st.markdown("### Top User Data - Master Level")
            else:
                df = get_top_insurance(year_val, quarter_val)
                st.markdown("### Top Insurance Data - Master Level")

        elif data_level == "District Level":
            if data_type == "Transactions":
                df = analytics.get_top_transaction_districts_wise_data(year_val, quarter_val)
                st.markdown("### Top Transaction Data - District Level")
            elif data_type == "Users":
                df = analytics.get_top_user_districts_wise_data(year_val, quarter_val)
                st.markdown("### Top User Data - District Level")
            else:
                df = analytics.get_top_insurance_districts_wise_data(year_val, quarter_val)
                st.markdown("### Top Insurance Data - District Level")
        
        else:  # Pincode Level
            if data_type == "Transactions":
                df = analytics.get_top_transaction_pincode_wise_data(year_val, quarter_val)
                st.markdown("### Top Transaction Data - Pincode Level")
            elif data_type == "Users":
                df = analytics.get_top_user_pincode_wise_data(year_val, quarter_val)
                st.markdown("### Top User Data - Pincode Level")
            else:
                df = analytics.get_top_insurance_pincode_wise_data(year_val, quarter_val)
                st.markdown("### Top Insurance Data - Pincode Level")
    
    if not df.empty:
        # Show stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Total Records</div>
                    <div class="metric-value">{len(df):,}</div>
                </div>
            ''', unsafe_allow_html=True)

        with col2:
            st.markdown(f'''
                <div class="metric-card">
                    <div class="metric-label">Total Columns</div>
                    <div class="metric-value">{len(df.columns)}</div>
                </div>
            ''', unsafe_allow_html=True)

        with col3:
            # Show additional metric based on data type
            if data_type == "Transactions" and 'total_trans_amount' in df.columns:
                total_amount = df['total_trans_amount'].sum() / 10000000
                st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-label">Total Amount</div>
                        <div class="metric-value">₹ {total_amount:.2f} Cr</div>
                    </div>
                ''', unsafe_allow_html=True)
            elif data_type == "Users" and 'total_registered_users' in df.columns:
                total_users = df['total_registered_users'].sum() / 10000000
                st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-label">Total Users</div>
                        <div class="metric-value">{total_users:.2f} Cr</div>
                    </div>
                ''', unsafe_allow_html=True)
            elif data_type == "Insurance" and 'total_insurance_amount' in df.columns:
                total_ins = df['total_insurance_amount'].sum() / 10000000
                st.markdown(f'''
                    <div class="metric-card">
                        <div class="metric-label">Total Insurance</div>
                        <div class="metric-value">₹ {total_ins:.2f} Cr</div>
                    </div>
                ''', unsafe_allow_html=True)
        
        # Show data
        st.markdown("<br>", unsafe_allow_html=True)        
        st.dataframe(df, use_container_width=True, height=500)

    else:
        st.warning("No data available for selected filters.")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==================== INSIGHTS TAB ====================
with tabs[5]:
    st.markdown('<h2 class="section-header">Key Insights & Recommendations</h2>', unsafe_allow_html=True)
    
    # Get data safely
    summary_df_insights = analytics.get_executive_summary(year_val, quarter_val)
    
    if not summary_df_insights.empty:
        summary = summary_df_insights.iloc[0]
        top_states = analytics.get_top_states_by_transaction_amount(year_val, quarter_val, limit=5)

        st.markdown("### Data-Driven Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Transaction insights
            trans_growth = analytics.get_year_over_year_growth()
            if not trans_growth.empty and len(trans_growth) > 1:
                latest_growth = trans_growth.iloc[-1]['amount_growth']
                if pd.notna(latest_growth):
                    st.success(f"YoY Growth: **{latest_growth:.1f}%**")
                else:
                    st.info("Growth metrics will be available with more data")
            
            # Device insights
            device_df = analytics.get_device_brand_popularity(year_val)
            if not device_df.empty:
                top_brand = device_df.iloc[0]['device_brand']
                st.info(f"Most Popular Device: **{top_brand}**")
        
        with col2:
            # User engagement insights
            engagement_df = analytics.get_user_engagement_metrics(year_val, quarter_val)
            if not engagement_df.empty and not engagement_df['avg_opens_per_user'].isna().all():
                avg_engagement = engagement_df['avg_opens_per_user'].mean()
                st.success(f"Avg User Engagement: **{avg_engagement:.1f}x** app opens per user")
            
            # Insurance insights
            insurance_df = analytics.get_insurance_adoption_by_state(year_val, quarter_val)
            if not insurance_df.empty:
                total_ins = insurance_df['insur_amount'].sum() / 10000000
                st.info(f"Total Insurance: **₹ {total_ins:.2f} Cr**")
        
        st.markdown("""
            <div class="insight-box">
                <div class="insight-title">Market Overview</div>
                <div class="insight-text">
                    PhonePe has demonstrated strong digital payment adoption across India. 
                    The platform shows consistent growth in transaction volumes and user engagement,
                    indicating increasing trust in digital payment systems.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if not top_states.empty:
            top_state = top_states.iloc[0]['state']
            top_amount = top_states.iloc[0]['trans_amount'] / 10000000
            
            st.markdown(f"""
                <div class="insight-box">
                    <div class="insight-title">Top Performer</div>
                    <div class="insight-text">
                        <strong>{top_state}</strong> leads in transaction volume with ₹ {top_amount:.2f} Crores, 
                        showing strong digital payment adoption.
                        Focus on replicating success factors to other states.
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        # Calculate some insights
        total_amount = summary.get('total_transaction_amount', 0) or 0
        total_users = summary.get('total_users', 0) or 0
        
        if total_amount > 0 and total_users > 0:
            amount_per_user = (total_amount / total_users)
            
            st.markdown(f"""
                <div class="insight-box">
                    <div class="insight-title">Key Metrics</div>
                    <div class="insight-text">
                        -  Average transaction value per user: <strong>₹ {amount_per_user:.0f}</strong><br>
                        -  Total transaction amount: <strong>₹ {total_amount/10000000:.2f} Crores</strong><br>
                        -  Total registered users: <strong>{total_users/10000000:.2f} Crores</strong>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="insight-box">
                <div class="insight-title">Growth Opportunities</div>
                <div class="insight-text">
                    -  <strong>Insurance Expansion:</strong> Expand insurance product offerings in high-transaction states<br>
                    -  <strong>User Engagement:</strong> Increase engagement through targeted campaigns and gamification<br>
                    -  <strong>Market Penetration:</strong> Focus on tier-2 and tier-3 cities for user base expansion<br>
                    -  <strong>Performance:</strong> Optimize app performance for better user retention<br>
                    -  <strong>Device Strategy:</strong> Partner with popular mobile brands for better reach
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="insight-box">
                <div class="insight-title">Business Recommendations</div>
                <div class="insight-text">
                    <strong>1. Customer Segmentation:</strong> Tailor marketing strategies based on spending patterns and user behavior<br><br>
                    <strong>2. Fraud Detection:</strong> Implement advanced analytics to identify unusual transaction patterns and prevent fraud<br><br>
                    <strong>3. Regional Focus:</strong> Develop state-specific features and campaigns based on local preferences<br><br>
                    <strong>4. Product Development:</strong> Leverage data insights for new feature development and service improvements<br><br>
                    <strong>5. Partnership Strategy:</strong> Collaborate with high-adoption regions for pilot programs
                </div>
            </div>
        """, unsafe_allow_html=True)
            
    else:
        st.warning("No data available for the selected period. Please select a different year/quarter to view insights.")
        
        st.markdown("""
            <div class="insight-box">
                <div class="insight-title">General Insights About PhonePe Pulse</div>
                <div class="insight-text">
                    PhonePe Pulse provides comprehensive data on digital payment trends across India, including:
                    <ul>
                        <li>Transaction volumes and amounts by state, district, and pincode</li>
                        <li>User registration and app engagement metrics</li>
                        <li>Insurance product adoption and growth</li>
                        <li>Device brand preferences among users</li>
                        <li>Quarterly and yearly growth trends</li>
                    </ul>
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p style='font-size: 0.9rem;'>PhonePe Pulse Data Visualization Dashboard</p>
        <p style='font-size: 0.8rem;'>Data sourced from PhonePe Pulse | Built with Streamlit & Plotly</p>
    </div>
""", unsafe_allow_html=True)