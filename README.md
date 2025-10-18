# Project PhonePe Pulse 

A comprehensive Streamlit-based analytics dashboard that visualizes digital payment trends across India using PhonePe Pulse data. This interactive platform provides state-wise transaction insights, user engagement metrics, insurance analytics, and quarterly trends through dynamic Plotly visualizations and choropleth maps.

Built with Python, Streamlit, Pandas, SQLAlchemy, and Plotly Express, this dashboard delivers actionable insights into India's digital payment ecosystem with a modern glassmorphism UI theme.

---

## Project Structure

```
Project_Phonepe/
│
├── app.py                          # Main Streamlit application entry point
├── requirements.txt                # Python package dependencies
├── .env                            # Environment variables (DB credentials)
├── .gitignore                      # Git ignore rules
├── pyvenv.cfg                      # Virtual environment configuration
│
├── src/
│   ├── sql/
│   │   ├── sql_queries.py          # Raw SQL query functions for fetching table data
│   │   └── sql_analysis.py         # PhonePeAnalytics class with business intelligence queries
│   │   └── create_table.sql        # MySQL database schema creation script
│   │
│   ├── etl/
│   │   ├── etl_aggregate.py        # ETL pipeline for aggregated transaction/user/insurance data
│   │   ├── etl_map.py              # ETL pipeline for district-level map data
│   │   └── etl_top.py              # ETL pipeline for top-level state/district/pincode data
│   │
│   ├── icon/
│   │   └── favicon.ico             # Application favicon
│   │
│   ├── config.py                   # Database connection configuration using SQLAlchemy
│   └── visualization.py            # Plotly visualization functions (maps, charts, graphs)
│
└── pulse/
    └── data/                       # PhonePe Pulse JSON data files
        ├── aggregated/             # State-level aggregated data
        ├── map/                    # District-level hover data
        └── top/                    # Top entities (states, districts, pincodes)

```

---

## Installation & Setup

### Prerequisites
- Python 3.13 or higher
- MySQL Server
- Git (optional, for cloning)

### Steps

1. **Clone or download the project**
   ```bash
   git clone https://github.com/Jashabant-Behera/Project-Phonepe.git
   cd Project_Phonepe
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     env\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure database credentials**
   
   Create a `.env` file in the root directory:
   ```env
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=phonepe
   ```

6. **Create database schema**
   ```bash
   mysql -u root -p < create_table.sql
   ```

7. **Run ETL pipelines to load data**
   ```bash
   python src/etl/etl_aggregate.py
   python src/etl/etl_map.py
   python src/etl/etl_top.py
   ```

---

## Running the App

Start the Streamlit dashboard:
```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`, displaying:
- Executive summary dashboard with key metrics
- Interactive state-wise transaction maps
- Quarterly trend analysis
- User engagement analytics
- Device brand distribution
- Insurance adoption metrics
- Raw data explorer with filters

---

## Key Features

### Executive Summary Dashboard
- Total transaction amount, count, and average transaction value
- Registered users and app opens metrics
- Insurance policy count and total coverage amount
- Top performing states visualization

### Transaction Analytics
- Transaction type distribution (Peer-to-peer, Merchant payments, Recharge & bill payments, etc.)
- Quarterly comparison charts
- Interactive India choropleth map showing state-wise transaction density
- Top districts analysis with drill-down capability

### User Analytics
- User engagement metrics (app opens per user)
- Device brand popularity analysis
- User growth trends over time
- State-wise user distribution

### Insurance Analytics
- State-wise insurance adoption rates
- Average policy values
- Insurance amount distribution map
- Total policies issued metrics

### Data Explorer
- Raw table data viewer with year/quarter filters
- Support for all 9 database tables (aggregated, map, and top-level data)
- Statistical summaries for numerical columns
- Export-ready dataframes

### Advanced SQL Analytics
- Year-over-year growth calculations
- Top states/districts by transaction volume
- Device brand market share analysis
- Quarterly performance comparisons

---

## Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Web application framework for building interactive dashboards |
| **Pandas** | Data manipulation, transformation, and analysis |
| **Plotly Express** | Interactive visualizations (bar charts, pie charts, line graphs) |
| **Plotly Graph Objects** | Advanced choropleth maps and custom charts |
| **SQLAlchemy** | Database ORM and connection management |
| **MySQL Connector** | MySQL database driver |
| **Python-dotenv** | Environment variable management for secure credentials |
| **NumPy** | Numerical computations |
| **Requests** | HTTP library for fetching GeoJSON data |

---

## Data & Database Info

### Data Source
The project uses **PhonePe Pulse** open data, containing digital payment transaction records across India from 2018-2022.

## Data Setup

This project requires PhonePe Pulse data which is not included in the repository.

### Download Data

1. Clone the PhonePe Pulse repository:
```bash
   git clone https://github.com/PhonePe/pulse.git
```

2. Copy the data folder:
```bash
   # Windows
   xcopy pulse\data .\pulse\data /E /I
   
   # macOS/Linux
   cp -r pulse/data ./pulse/data
```

3. Verify structure:
```
   pulse/
   └── data/
       ├── aggregated/
       ├── map/
       └── top/
```

## Database Setup

### Option A: Load from SQL Dump (Faster)

1. Create the database:
```bash
   mysql -u root -p -e "CREATE DATABASE phonepe;"
```

2. Import data:
```bash
   mysql -u root -p phonepe < phonepe_backup.sql
```

### Option B: Run ETL Scripts (Requires pulse/data folder)
See "Data Setup" section above.
```

---

## Complete Deployment Solution

Since you're deploying to Streamlit Cloud **without the data**, here's the best approach:

### Architecture Diagram
```
GitHub (Your Code)
    ↓
Streamlit Cloud (App)
    ↓
Cloud MySQL Database (Your Data)
    ↑
Your Local MySQL (Export from here)

### Load Data into Database

Run the ETL scripts in order:
```bash
python src/etl/etl_aggregate.py
python src/etl/etl_map.py
python src/etl/etl_top.py
```

### Database Schema
The MySQL database `phonepe` contains 9 tables:

**Aggregated Tables:**
- `aggr_transaction` – State-level transaction data by type
- `aggr_user` – Registered users, app opens, and device brand distribution
- `aggr_insurance` – Insurance transaction aggregates

**Map-Level Tables:**
- `map_transaction` – District-level transaction hover data
- `map_user` – District-level user metrics
- `map_insurance` – District-level insurance data

**Top-Level Tables:**
- `top_transaction` – Top states, districts, and pincodes by transaction volume
- `top_user` – Top entities by registered users
- `top_insurance` – Top insurance adoption locations

### ETL Pipeline
1. **Extraction:** JSON files are read from the `pulse/data/` directory structure
2. **Transformation:** Data is cleaned, normalized, and aggregated using Pandas
3. **Loading:** Transformed data is inserted into MySQL tables via SQLAlchemy

---

## UI & Theme

The dashboard features a custom **dark glassmorphism theme** with:
- **Color Palette:** Deep purple gradient background (radial from `#2C034A` to black)
- **Accent Colors:** Purple gradient (`#7b61ff` to `#9d8eff`)
- **Typography:** Inter font family with antialiased rendering
- **Visual Effects:**
  - Frosted glass panels with backdrop blur
  - Hover lift animations on cards
  - Gradient-accented headings using background-clip
  - Custom scrollbar styling
  - Responsive design with mobile breakpoints
- **Components:**
  - Glassmorphic metric cards with gradient values
  - Styled input controls with focus states
  - Tab navigation with selected state highlighting
  - Professional data tables with hover effects

---

## Code Overview

### Backend Architecture

**Database Layer (`config.py`)**
- SQLAlchemy engine initialization
- Environment variable loading via `python-dotenv`
- Connection pooling and session management

**Data Access Layer (`sql_queries.py`)**
- Parameterized SQL query functions with injection prevention
- Table whitelist validation
- Year/quarter filtering support

**Analytics Layer (`sql_analysis.py`)**
- `PhonePeAnalytics` class encapsulating business intelligence queries
- Methods for executive summaries, growth calculations, and comparative analysis
- Safe NULL handling with COALESCE
- Window functions for year-over-year metrics

**Visualization Layer (`visualization.py`)**
- State name mapping for GeoJSON compatibility
- Plotly Express and Graph Objects wrappers
- Consistent theme application across all charts
- Functions: `plot_india_choropleth()`, `plot_top_states_bar()`, `plot_transaction_type_distribution()`, etc.

### Frontend Architecture (`app.py`)

**Component Structure:**
1. **Page Configuration:** Wide layout with custom favicon
2. **CSS Injection:** 500+ lines of custom styling
3. **Sidebar Filters:** Year and quarter selectors
4. **Tab Navigation:** 6 main sections (Overview, Transactions, Users, Insurance, Raw Data, Insights)
5. **Dynamic Content:** Conditional rendering based on filter selection
6. **Metric Cards:** Custom HTML components for KPIs

**Key Functions:**
- `safe_divide()` – Prevents division-by-zero errors in metric calculations
- `map_state_names()` – Normalizes state names for map rendering
- Filter propagation to all analytics queries

---

## Example Usage

### Querying Transaction Data
```python
from src.sql.sql_analysis import PhonePeAnalytics

# Initialize analytics engine
analytics = PhonePeAnalytics()

# Get top 5 states by transaction amount for Q3 2022
df = analytics.get_top_states_by_transaction_amount(year=2022, quarter=3, limit=5)
print(df[['state', 'trans_amount', 'trans_count']])
```

### Generating Visualizations
```python
from src.visualization import plot_india_choropleth
import pandas as pd

# Prepare state-wise data
state_data = pd.DataFrame({
    'state': ['Karnataka', 'Maharashtra', 'Tamil Nadu'],
    'trans_amount': [150000000, 200000000, 120000000]
})

# Create choropleth map
fig = plot_india_choropleth(state_data, 'trans_amount', 'Transaction Distribution', 'Purples')
fig.show()
```

### Fetching Raw Data
```python
from src.sql.sql_queries import get_aggr_transaction

# Get all transactions for 2021 Q4
df = get_aggr_transaction(year=2021, quarter=4)
print(df.info())
```

---

## Customization

### Updating Database Credentials
Edit the `.env` file to change connection parameters:
```env
DB_HOST=your_host
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=your_database
```

### Modifying Year/Quarter Filters
In `app.py`, update the filter options:
```python
year_options = ["All", 2018, 2019, 2020, 2021, 2022, 2023]  # Add new years
quarter_options = ["All", 1, 2, 3, 4]
```

### Customizing Visualizations
Modify color schemes in `visualization.py`:
```python
color_continuous_scale='Viridis'  # Change to 'Blues', 'Greens', etc.
```

### Adding New Metrics
Extend the `PhonePeAnalytics` class in `sql_analysis.py`:
```python
def get_custom_metric(self, year=None):
    query = "SELECT ... FROM ..."
    return pd.read_sql(query, self.engine, params=(year,))
```


---


