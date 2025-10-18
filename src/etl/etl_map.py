import os
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from src.config import engine

# Path
base_path = "pulse/data/map"

# ========================== Transaction Data ==========================
path_trans = os.path.join(base_path, 'transaction/hover/country/india/state')
states = os.listdir(path_trans)

trans_data = {
    'year': [], 'quarter': [], 'state': [], 'district':[],
    'trans_type': [], 'trans_count': [], 'trans_amount': []
}

for state in states:
    state_path = os.path.join(path_trans,state)
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path,year)
        for quarter_file in os.listdir(year_path):
            if quarter_file.endswith('.json'):
                quarter = int(quarter_file.strip('.json'))
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                for record in data['data'].get('hoverDataList',[]):
                    trans_data['year'].append(int(year))
                    trans_data['quarter'].append(quarter)
                    trans_data['state'].append(state)
                    trans_data['district'].append(record['name'])
                    trans_data['trans_type'].append(record['metric'][0]['type'])
                    trans_data['trans_count'].append(record['metric'][0]['count'])
                    trans_data['trans_amount'].append(record['metric'][0]['amount'])

# Load to DataFrame and SQL
df_trans = pd.DataFrame(trans_data)

df_trans.to_sql('map_transaction', con=engine, if_exists='append', index=False)
print("Transaction data loaded successfully.")

# ========================== User Data ==========================
user_path = os.path.join(base_path, 'user/hover/country/india/state')
user_data = {
    'year': [], 'quarter': [], 'state': [], 'district':[],
    'registered_user': [], 'app_opens': []
}

for state in os.listdir(user_path):
    state_path = os.path.join(user_path, state)
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        for quarter_file in os.listdir(year_path):
            if quarter_file.endswith('.json'):
                quarter = int(quarter_file.strip('.json'))
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as f:
                    data = json.load(f)

                for region_name, region_data in data['data'].get('hoverData',{}).items():
                    user_data['year'].append(int(year))
                    user_data['quarter'].append(quarter)
                    user_data['state'].append(state)
                    user_data['district'].append(region_name)
                    user_data['registered_user'].append(region_data.get('registeredUsers', 0))
                    user_data['app_opens'].append(region_data.get('appOpens', 0))
                    
df_user = pd.DataFrame(user_data)

df_user.to_sql('map_user', con=engine, if_exists='append', index=False)
print("User data loaded successfully.")


# ========================== Insurance Data ==========================
insurance_path = os.path.join(base_path, 'insurance/hover/country/india/state')
insurance_data = {
    'year': [], 'quarter': [], 'state': [],
    'insurance_type': [], 'insurance_count': [], 'insurance_amount': []
}

for state in os.listdir(insurance_path):
    state_path = os.path.join(insurance_path, state)
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        for quarter_file in os.listdir(year_path):
            if quarter_file.endswith('.json'):
                quarter = int(quarter_file.strip('.json'))
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                for record in data['data'].get('hoverDataList', []):
                    insurance_data['year'].append(int(year))
                    insurance_data['quarter'].append(quarter)
                    insurance_data['state'].append(record['name'])
                    insurance_data['insurance_type'].append(record.get('metric', [{}])[0].get('type', 0))
                    insurance_data['insurance_count'].append(record.get('metric', [{}])[0].get('count', 0))
                    insurance_data['insurance_amount'].append(record.get('metric', [{}])[0].get('amount', 0))
                    
df_insurance = pd.DataFrame(insurance_data)

df_insurance.to_sql('map_insurance', con=engine, if_exists='append', index=False)
print("Insurance data loaded successfully.")