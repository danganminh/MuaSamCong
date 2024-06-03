import pandas as pd
from io import StringIO

from functions.logic import wait_dual_data, convert_str_to_dtype, get_value


def processing_BienBanMoThau(driver, MA_TBMT, ID_TBMT):
    
    print(f'Processing BienBanMoThau {MA_TBMT}')

    columns_1 = ['Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (nếu có) (VND)', 'Hiệu lực báo giá (ngày)', 'Thời gian giao hàng']
    df_1 = pd.DataFrame(columns=columns_1)

    columns_2 = ['Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (nếu có) (VND)', 'Hiệu lực E-HSDT (ngày)', 'Giá trị bảo đảm dự thầu (VND)', 'Hiệu lực bảo đảm dự thầu (ngày)', 'Thời gian thực hiện hợp đồng']
    df_2 = pd.DataFrame(columns=columns_2)

    columns_3 = ['Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (nếu có) (VND)', 'Hiệu lực E-HSDT (ngày)', 'Giá trị bảo đảm dự thầu (VND)', 'Hiệu lực bảo đảm dự thầu (ngày)', 'Thời gian giao hàng']
    df_3 = pd.DataFrame(columns=columns_3)
    
    columns_4 = ['Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (nếu có) (VND)', 'Hiệu lực E-HSDT (ngày)', 'Giá trị bảo đảm dự thầu (VND)', 'Hiệu lực bảo đảm dự thầu (ngày)', 'Thời gian thực hiện gói thầu']
    df_4 = pd.DataFrame(columns=columns_4)
    
    columns_5 = ['Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (nếu có) (VND)', 'Hiệu lực báo giá (ngày)', 'Thời gian thực hiện hợp đồng']
    df_5 = pd.DataFrame(columns=columns_5)
    
    df_all = pd.DataFrame()

    data_1 = []
    data_2 = []
    data_3 = []
    data_4 = []
    data_5 = []

    wait_dual_data(driver, xpath_left='//*[@id="bidOpeningMinutes"]/div[1]/div[2]/div/div[1]', xpath_right='//*[@id="bidOpeningMinutes"]/div[1]/div[2]/div/div[2]')
    
    # Find table
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
            if len(table.columns) == len(columns_5) and all(table.columns == columns_5):
                data_5 = table.values.tolist()
                break
        except:
            continue

    thoidiemhoanthanhmothau = get_value(driver, key='Thời điểm hoàn thành mở thầu', xpath_key='//*[@id="bidOpeningMinutes"]/div[1]/div[2]')

    for i in range(len(data_1)):
        df_1.loc[i] = data_1[i]

    for j in range(len(data_2)):
        df_2.loc[j] = data_2[j]
    
    for j in range(len(data_3)):
        df_3.loc[j] = data_3[j]
        
    for j in range(len(data_4)):
        df_4.loc[j] = data_4[j]
        
    for j in range(len(data_5)):
        df_5.loc[j] = data_5[j]

    df_all = pd.concat([df_all, df_1], ignore_index=True)
    df_all = pd.concat([df_all, df_2], ignore_index=True)
    df_all = pd.concat([df_all, df_3], ignore_index=True)
    df_all = pd.concat([df_all, df_4], ignore_index=True)
    df_all = pd.concat([df_all, df_5], ignore_index=True)

    # Change type of data
    df_all['Giá dự thầu (VND)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df_all['Giá dự thầu (VND)'].values]
    df_all['Tỷ lệ giảm giá (%)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df_all['Tỷ lệ giảm giá (%)'].values]
    df_all['Giá dự thầu sau giảm giá (nếu có) (VND)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df_all['Giá dự thầu sau giảm giá (nếu có) (VND)'].values]
    df_all['Giá trị bảo đảm dự thầu (VND)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df_all['Giá trị bảo đảm dự thầu (VND)'].values]
    df_all['Hiệu lực bảo đảm dự thầu (ngày)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df_all['Hiệu lực bảo đảm dự thầu (ngày)'].values]


    remane_list = {
        'id': [None for _ in range(len(df_all))],
        'Ma_TBMT': [MA_TBMT for _ in range(len(df_all))],
        'ID_TBMT': [ID_TBMT for _ in range(len(df_all))],
        'contractorCode_final': df_all['Mã định danh'].values,
        'contractorName_final': df_all['Tên nhà thầu'].values,
        'bidPrice': df_all['Giá dự thầu (VND)'].values,
        'bidPriceUnit': ['VND' if val else None for val in df_all['Giá dự thầu (VND)'].values],
        'saleNumber': df_all['Tỷ lệ giảm giá (%)'].values,
        'bidFinalPrice': df_all['Giá dự thầu sau giảm giá (nếu có) (VND)'].values,
        'bidGuarantee': df_all['Giá trị bảo đảm dự thầu (VND)'].values,
        'bidGuaranteeValidity': df_all['Hiệu lực bảo đảm dự thầu (ngày)'].values,
        'NewContractPeriod': df_all['Thời gian giao hàng'].values,
        'createdDateBidOpen': [thoidiemhoanthanhmothau if thoidiemhoanthanhmothau else None for _ in range(len(df_all))]
    }   
    
    BIENBAN_MOTHAU_DF = pd.DataFrame(remane_list)
    
    return BIENBAN_MOTHAU_DF