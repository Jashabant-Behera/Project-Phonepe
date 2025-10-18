import os
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from src.config import engine

# Path
base_path = "pulse/data/aggregated"

# ========================== Transaction Data ==========================
path_trans = os.path.join(base_path, 'transaction/country/india/state')
states = os.listdir(path_trans)

trans_data = {
    'year': [], 'quarter': [], 'state': [],
    'trans_type': [], 'trans_count': [], 'trans_amount': []
}

for state in states:
    state_path = os.path.join(path_trans, state)
    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)
        for quarter_file in os.listdir(year_path):
            if quarter_file.endswith('.json'):
                quarter = int(quarter_file.strip('.json'))
                file_path = os.path.join(year_path, quarter_file)
                with open(file_path, 'r') as f:
                    data = json.load(f)
                for record in data['data'].get('transactionData', []):
                    trans_data['year'].append(int(year))
                    trans_data['quarter'].append(quarter)
                    trans_data['state'].append(state)
                    trans_data['trans_type'].append(record['name'])
                    trans_data['trans_count'].append(record['paymentInstruments'][0]['count'])
                    trans_data['trans_amount'].append(record['paymentInstruments'][0]['amount'])

# Load to DataFrame and SQL
df_trans = pd.DataFrame(trans_data)

df_trans.to_sql('aggr_transaction', con=engine, if_exists='append', index=False)
print("Transaction data loaded successfully.")

# ========================== User Data ==========================
user_path = os.path.join(base_path, 'user/country/india/state')
user_data = {
    'year': [], 'quarter': [], 'state': [],
    'registered_user': [], 'app_opens': [],
    'device_brand': [], 'device_count': [], 'device_percentage': []
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

                for device in data['data'].get('usersByDevice') or []:
                    user_data['year'].append(int(year))
                    user_data['quarter'].append(quarter)
                    user_data['state'].append(state)
                    user_data['registered_user'].append(data['data'].get('aggregated', {}).get('registeredUsers', 0))
                    user_data['app_opens'].append(data['data'].get('aggregated', {}).get('appOpens', 0))
                    user_data['device_brand'].append(device.get('brand', ''))
                    user_data['device_count'].append(device.get('count', 0))
                    user_data['device_percentage'].append(device.get('percentage', 0.0))


df_user = pd.DataFrame(user_data)

df_user.to_sql('aggr_user', con=engine, if_exists='append', index=False)
print("User data loaded successfully.")

# ========================== Insurance Data ==========================
insurance_path = os.path.join(base_path, 'insurance/country/india/state')
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
                for record in data['data'].get('transactionData', []):
                    insurance_data['year'].append(int(year))
                    insurance_data['quarter'].append(quarter)
                    insurance_data['state'].append(state)
                    insurance_data['insurance_type'].append(record['name'])
                    insurance_data['insurance_count'].append(record.get('paymentInstruments', [{}])[0].get('count', 0))
                    insurance_data['insurance_amount'].append(record.get('paymentInstruments', [{}])[0].get('amount', 0))
                    
df_insurance = pd.DataFrame(insurance_data)

df_insurance.to_sql('aggr_insurance', con=engine, if_exists='append', index=False)
print("Insurance data loaded successfully.")