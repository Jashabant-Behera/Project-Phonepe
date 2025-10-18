import os
import json
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from src.config import engine

base_path = "pulse/data/top"

# ======== Transaction Data ========
path_trans = os.path.join(base_path, 'transaction/country/india/state')
states = os.listdir(path_trans)

trans_data = {
    'year': [], 'quarter': [], 'state': [], 'district': [], 'pincode': [],
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

                # states, districts and pincodes separately
                for record in data['data'].get('states') or []:
                    trans_data['year'].append(int(year))
                    trans_data['quarter'].append(quarter)
                    trans_data['state'].append(record.get('entityName', ''))
                    trans_data['district'].append('')
                    trans_data['pincode'].append('')
                    metric = record.get('metric', {})
                    trans_data['trans_type'].append(metric.get('type', ''))
                    trans_data['trans_count'].append(metric.get('count', 0))
                    trans_data['trans_amount'].append(metric.get('amount', 0.0))

                for record in data['data'].get('districts') or []:
                    trans_data['year'].append(int(year))
                    trans_data['quarter'].append(quarter)
                    trans_data['state'].append(state)
                    trans_data['district'].append(record.get('entityName', ''))
                    trans_data['pincode'].append('')
                    metric = record.get('metric', {})
                    trans_data['trans_type'].append(metric.get('type', ''))
                    trans_data['trans_count'].append(metric.get('count', 0))
                    trans_data['trans_amount'].append(metric.get('amount', 0.0))

                for record in data['data'].get('pincodes') or []:
                    trans_data['year'].append(int(year))
                    trans_data['quarter'].append(quarter)
                    trans_data['state'].append(state)
                    trans_data['district'].append('')
                    trans_data['pincode'].append(record.get('entityName', ''))
                    metric = record.get('metric', {})
                    trans_data['trans_type'].append(metric.get('type', ''))
                    trans_data['trans_count'].append(metric.get('count', 0))
                    trans_data['trans_amount'].append(metric.get('amount', 0.0))


df_trans = pd.DataFrame(trans_data)
df_trans.to_sql('top_transaction', con=engine, if_exists='append', index=False)
print("Transaction data loaded successfully.")


# ======== User Data ========
user_path = os.path.join(base_path, 'user/country/india/state')
user_data = {
    'year': [], 'quarter': [], 'state': [], 'district': [], 'pincode': [],
    'registered_user': []
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

                for record in data['data'].get('states') or []:
                    user_data['year'].append(int(year))
                    user_data['quarter'].append(quarter)
                    user_data['state'].append(record.get('entityName', ''))
                    user_data['district'].append('')
                    user_data['pincode'].append('')
                    user_data['registered_user'].append(record.get('registeredUsers', 0))

                for record in data['data'].get('districts') or []:
                    user_data['year'].append(int(year))
                    user_data['quarter'].append(quarter)
                    user_data['state'].append(state)
                    user_data['district'].append(record.get('entityName', ''))
                    user_data['pincode'].append('')
                    user_data['registered_user'].append(record.get('registeredUsers', 0))

                for record in data['data'].get('pincodes') or []:
                    user_data['year'].append(int(year))
                    user_data['quarter'].append(quarter)
                    user_data['state'].append(state)
                    user_data['district'].append('')
                    user_data['pincode'].append(record.get('entityName', ''))
                    user_data['registered_user'].append(record.get('registeredUsers', 0))


df_user = pd.DataFrame(user_data)
df_user.to_sql('top_user', con=engine, if_exists='append', index=False)
print("User data loaded successfully.")


# ======== Insurance Data ========
insurance_path = os.path.join(base_path, 'insurance/country/india/state')
insurance_data = {
    'year': [], 'quarter': [], 'state': [], 'district': [], 'pincode': [],
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

                for record in data['data'].get('states') or []:
                    insurance_data['year'].append(int(year))
                    insurance_data['quarter'].append(quarter)
                    insurance_data['state'].append(record.get('entityName', ''))
                    insurance_data['district'].append('')
                    insurance_data['pincode'].append('')
                    metric = record.get('metric', {})
                    insurance_data['insurance_type'].append(metric.get('type', ''))
                    insurance_data['insurance_count'].append(metric.get('count', 0))
                    insurance_data['insurance_amount'].append(metric.get('amount', 0.0))

                for record in data['data'].get('districts') or []:
                    insurance_data['year'].append(int(year))
                    insurance_data['quarter'].append(quarter)
                    insurance_data['state'].append(state)
                    insurance_data['district'].append(record.get('entityName', ''))
                    insurance_data['pincode'].append('')
                    metric = record.get('metric', {})
                    insurance_data['insurance_type'].append(metric.get('type', ''))
                    insurance_data['insurance_count'].append(metric.get('count', 0))
                    insurance_data['insurance_amount'].append(metric.get('amount', 0.0))

                for record in data['data'].get('pincodes') or []:
                    insurance_data['year'].append(int(year))
                    insurance_data['quarter'].append(quarter)
                    insurance_data['state'].append(state)
                    insurance_data['district'].append('')
                    insurance_data['pincode'].append(record.get('entityName', ''))
                    metric = record.get('metric', {})
                    insurance_data['insurance_type'].append(metric.get('type', ''))
                    insurance_data['insurance_count'].append(metric.get('count', 0))
                    insurance_data['insurance_amount'].append(metric.get('amount', 0.0))

df_insurance = pd.DataFrame(insurance_data)
df_insurance.to_sql('top_insurance', con=engine, if_exists='append', index=False)
print("Insurance data loaded successfully.")