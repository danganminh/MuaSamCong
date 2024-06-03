import pandas as pd
from io import StringIO

from functions.logic import convert_str_to_dtype, wait_dual_data

def processing_HSDXTC(driver, MA_TBMT, ID_TBMT):

    print(f'Processing HSDXTC {MA_TBMT}')

    columns_1 = ['Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (VND)', 'Điểm kỹ thuật', 'Hiệu lực E-HSĐXTC (ngày)']
    columns_2 = ['Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (VND)', 'Điểm kỹ thuật', 'Hiệu lực E-HSDXTC (ngày)']
    columns_3 = ['Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (VND)', 'Hiệu lực E-HSĐXTC (ngày)']
    columns_4 = ['Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (VND)', 'Hiệu lực E-HSDXTC (ngày)']
    
    df_1 = pd.DataFrame(columns=columns_1)
    df_2 = pd.DataFrame(columns=columns_2)
    df_3 = pd.DataFrame(columns=columns_3) 
    df_4 = pd.DataFrame(columns=columns_4)
    
    df = pd.DataFrame()

    data_1 = []
    data_2 = []
    data_3 = []
    data_4 = []

    wait_dual_data(driver, xpath_left='//*[@id="hsdxtc"]/div[1]/div[2]/div/div[1]', xpath_right='//*[@id="hsdxtc"]/div[1]/div[2]/div/div[2]')
    all_table = pd.read_html(StringIO(driver.page_source))
    for table in all_table:
        try:
            if len(table.columns) == len(columns_1) and all(table.columns == columns_1):
                data_1 = table.values.tolist()
                break
            if len(table.columns) == len(columns_2) and all(table.columns == columns_2):
                data_2 = table.values.tolist()
                break
            if len(table.columns) == len(columns_3) and all(table.columns == columns_3):
                data_3 = table.values.tolist()
                break
            if len(table.columns) == len(columns_4) and all(table.columns == columns_4):
                data_4 = table.values.tolist()
                break
        except:
            continue

    for i in range(len(data_1)):
        df_1.loc[i] = data_1[i]
    for i in range(len(data_2)):
        df_2.loc[i] = data_2[i]
    for i in range(len(data_3)):
        df_3.loc[i] = data_3[i]
    for i in range(len(data_4)):
        df_4.loc[i] = data_4[i]


    df = pd.concat([df, df_1], ignore_index=True)
    df = pd.concat([df, df_2], ignore_index=True)
    df = pd.concat([df, df_3], ignore_index=True)
    df = pd.concat([df, df_4], ignore_index=True)

    df['Hieu luc'] = df['Hiệu lực E-HSĐXTC (ngày)'].combine_first(df['Hiệu lực E-HSDXTC (ngày)'])
        
    # Convert data type
    df['Giá dự thầu (VND)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df['Giá dự thầu (VND)'].values]
    df['Tỷ lệ giảm giá (%)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df['Tỷ lệ giảm giá (%)'].values]
    df['Giá dự thầu sau giảm giá (VND)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df['Giá dự thầu sau giảm giá (VND)'].values]
    df['Điểm kỹ thuật'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df['Điểm kỹ thuật'].values]
    
    
    rename_list = {
        'id': [None for _ in range(len(df))],
        'Ma_TBMT': [MA_TBMT for _ in range(len(df))],
        'ID_TBMT': [ID_TBMT for _ in range(len(df))],
        'contractorCode_final': df['Mã định danh'].values,
        'contractorName_final': df['Tên nhà thầu'].values,
        'bidPrice': df['Giá dự thầu (VND)'].values,
        'bidPriceUnit': ['VND' for _ in range(len(df))],
        'saleNumber': df['Tỷ lệ giảm giá (%)'].values,
        'bidFinalPrice': df['Giá dự thầu sau giảm giá (VND)'].values,
        'bidGuarantee': [None for _ in range(len(df))],
        'bidGuaranteeValidity': df['Hieu luc'].values,
        'techScore': df['Điểm kỹ thuật'].values,
        'NewContractPeriod': [None for _ in range(len(df))]
    }


    HSDXTC = pd.DataFrame(rename_list)
    
    return HSDXTC