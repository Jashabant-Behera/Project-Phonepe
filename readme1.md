# Project PhonePe Pulse

A Streamlit dashboard for exploring India’s digital payment trends using PhonePe Pulse data.  
It loads aggregated JSON data into a MySQL database and provides interactive charts and insights.  
Built with Streamlit, Pandas, Plotly, SQLAlchemy, and MySQL.

## Project Structure

The project follows this structure:

```
.
├── app.py
├── src
│   ├── config.py
│   ├── visualization.py
│   └── sql
│       ├── sql_analysis.py
│       └── sql_queries.py
├── create_table.sql
├── etl_aggregate.py
├── etl_map.py
├── etl_top.py
├── requirements.txt
├── .env
└── .gitignore
```

- **app.py** – Main Streamlit application launcher and UI definitions.  
- **src/config.py** – Loads environment variables and creates SQLAlchemy engine.  
- **src/visualization.py** – Defines Plotly chart and map functions.  
- **src/sql/sql_analysis.py** – Implements analytics queries in `PhonePeAnalytics` class.  
- **src/sql/sql_queries.py** – Provides generic table fetchers for raw data views.  
- **create_table.sql** – SQL DDL to create database and schema tables.  
- **etl_aggregate.py** – ETL script to load aggregated JSON into `aggr_*` tables.  
- **etl_map.py** – ETL script to load map-level JSON into `map_*` tables.  
- **etl_top.py** – ETL script to load top-level JSON into `top_*` tables.  
- **requirements.txt** – Lists Python dependencies.  
- **.env** – Stores database credentials (ignored by Git).  
- **.gitignore** – Specifies files and directories to ignore in Git.

## Installation & Setup

Follow these steps to prepare the project locally:

1. Clone the repo:  
   ```bash
   git clone https://github.com/yourusername/phonepe-pulse.git
   cd phonepe-pulse
   ```
2. Create and activate a virtual environment:  
   ```bash
   python -m venv env
   source env/bin/activate       # Linux/macOS
   env\Scripts\activate          # Windows
   ```
3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```
4. Configure database credentials:  
   - Copy `.env` file and fill your MySQL details.  
5. Initialize database schema:  
   ```bash
   mysql -u <user> -p < create_table.sql
   ```
6. Load data into MySQL:  
   ```bash
   python etl_aggregate.py
   python etl_map.py
   python etl_top.py
   ```

## Running the App

Launch the Streamlit dashboard with:

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.  
Use sidebar filters to explore year, quarter, state, and more.

## Key Features

- **Executive Summary**: Displays top metrics like transaction amount, user count, insurance adoption.  
- **Transaction Analytics**: Pie chart, bar chart, choropleth map, district-level drill-down.  
- **User Analytics**: Engagement rates, device brand popularity, growth trends.  
- **Insurance Analytics**: State-wise heatmap and policy metrics.  
- **Raw Data Explorer**: Load aggregated, map, or top-level tables as DataFrame.  
- **Insights & Recommendations**: Data-driven observations and actionable suggestions.

## Technologies Used

- **Python** – Core programming language.  
- **Streamlit** – Rapid UI development.  
- **Pandas** – Data processing and DataFrame operations.  
- **SQLAlchemy** – Database ORM and connection pooling.  
- **MySQL** – Relational database for storing analytics tables.  
- **python-dotenv** – Environment variable management.  
- **Plotly** – Interactive charts and maps.  
- **PyDeck** – Geospatial visualizations (imported for map layers).  
- **mysql-connector-python** – MySQL driver for Python.

## Data & Database Info

- **Data Source**: PhonePe Pulse JSON files under `pulse/data/{aggregated,map,top}`.  
- **Schema**: Defined in `create_table.sql` with tables for aggregated (`aggr_*`), map (`map_*`), and top (`top_*`) data.  
- **ETL**:  
  - `etl_aggregate.py` loads state-level aggregated data.  
  - `etl_map.py` loads district hover data for maps.  
  - `etl_top.py` loads state, district, and pincode metrics.  
- **Tables**:  
  - aggr_transaction, aggr_user, aggr_insurance  
  - map_transaction, map_user, map_insurance  
  - top_transaction, top_user, top_insurance

## UI & Theme

The app applies a **dark radial gradient** background with **glassmorphism** cards.  
It uses a **purple accent gradient** for headings and metrics.  
Typography loads the **Inter** font from Google Fonts for a modern look.

## Code Overview

- **app.py** orchestrates UI, filters, and tab layouts.  
- **PhonePeAnalytics** (in `sql_analysis.py`) runs SQL queries and returns DataFrames.  
- **visualization.py** defines reusable Plotly functions for charts and maps.  
- **sql_queries.py** fetches raw table data for the Raw Data Explorer.  
- **config.py** initializes the SQLAlchemy engine using `.env` credentials.  
- **ETL scripts** parse JSON files and use Pandas to load data into MySQL tables.

## Example Usage

```python
from src.sql.sql_analysis import PhonePeAnalytics

analytics = PhonePeAnalytics()
df_top_states = analytics.get_top_states_by_transaction_amount(year=2022, quarter=3)
print(df_top_states.head())
```

## Customization

- **Filters**: Change default `year_options` and `quarter_options` in `app.py`.  
- **Database**: Update `.env` credentials or database host/port.  
- **CSS**: Modify the `<style>` block in `app.py` to adjust colors and fonts.  
- **Charts**: Tweak color scales or labels in `visualization.py` functions.  
- **Data Paths**: Adjust `base_path` in ETL scripts if JSON files move.

---

By following this guide, you can set up, explore, and extend the PhonePe Pulse dashboard for deeper analytics and custom reporting.
