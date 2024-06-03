import time
import pandas as pd
from googleapiclient.discovery import build
from google.oauth2 import service_account
import logging

logging.basicConfig(level=logging.INFO)

gsheetId = '1lfkxn5sPh1lqTmyvUe3jSyXNXu2ZG0CSiMEuyId6TaE'

CLIENT_SA_SECRET_FILE = 'token-qldt.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']


def return_service():
    creds = service_account.Credentials.from_service_account_file(
        CLIENT_SA_SECRET_FILE, scopes=SCOPES
    )
    service = build(API_SERVICE_NAME, API_VERSION, credentials=creds, cache_discovery=False)
    return service


def get_data(range_data, gsheetId=gsheetId):
    result = return_service().spreadsheets().values().get(
        spreadsheetId=gsheetId, 
        range=range_data, 
        valueRenderOption='UNFORMATTED_VALUE'
    ).execute()
    values = result.get('values', [])
    if not values:
        logging.info(f'No data found in range {range_data}.')
        return pd.DataFrame()
    
    header = values[0]
    data = values[1:] if len(values) > 1 else []
    table = pd.DataFrame(data, columns=header)
    logging.info(f'Get data {range_data} successfully!')
    print(f'Get data {range_data} successfully!')
    return table

    
def append_gsheet(df, range_data, gsheetId=gsheetId):
    
    if df.empty:
        logging.warning(f'DataFrame {range_data} is empty. Nothing to append.')
        print(f'DataFrame {range_data} is empty. Nothing to append.')
        return

    df.fillna('', inplace=True)
    df = df.astype(str)

    # Skip headear
    values = df.T.reset_index().T.values.tolist()[1:]

    return_service().spreadsheets().values().append(
        spreadsheetId=gsheetId,
        range=range_data,
        valueInputOption='USER_ENTERED',
        body={
            "majorDimension": "ROWS",
            "values": values
        }
    ).execute()
    time.sleep(5)
    logging.info(f'Data successfully pushed to {range_data}!')
    print(f'Data successfully pushed to {range_data}!')


def update_gsheet(df, range_data, gsheetId=gsheetId):

    if df.empty:
        logging.warning('Both old and new DataFrames are empty. Nothing to update.')
        print('Both old and new DataFrames are empty. Nothing to update.')
        return

    df.fillna('', inplace=True)
    df = df.astype(str)

    return_service().spreadsheets().values().clear(spreadsheetId=gsheetId,range=range_data).execute()
        
    return_service().spreadsheets().values().update(
        spreadsheetId=gsheetId,
        range=range_data,
        valueInputOption='USER_ENTERED',
        body={
            "majorDimension": "ROWS",
            "values": df.T.reset_index().T.values.tolist()
        }
    ).execute()
    logging.info(f'Data successfully updated to {range_data}!')
    print(f'Data successfully updated to {range_data}!')

