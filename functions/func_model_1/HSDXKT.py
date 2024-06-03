import pandas as pd
from io import StringIO
from selenium.webdriver.common.by import By

from functions.logic import *

def processing_HSDXKT(driver, MA_TBMT, ID_TBMT, MaDinhDanh):

    HSDXKT_columns_v1 = ['Mã định danh', 'Tên nhà thầu', 'Hiệu lực HSDXKT (ngày)', 'Thời gian thực hiện hợp đồng']
    df_1_v1 = pd.DataFrame(columns=HSDXKT_columns_v1)
    HSDXKT_columns_v2 = ['Mã định danh', 'Tên nhà thầu', 'Hiệu lực HSĐXKT (ngày)', 'Thời gian thực hiện hợp đồng']
    df_1_v2 = pd.DataFrame(columns=HSDXKT_columns_v2)
    HSDXKT_columns_v3 = ['Mã định danh', 'Tên nhà thầu', 'Hiệu lực E-HSĐXKT (ngày)', 'Bảo đảm dự thầu (VND)', 'Hiệu lực của BĐDT (ngày)', 'Thời gian thực hiện hợp đồng']
    df_1_v3 = pd.DataFrame(columns=HSDXKT_columns_v3)
    HSDXKT_columns_v4 = ['Mã định danh', 'Tên nhà thầu', 'Hiệu lực E-HSDXKT (ngày)', 'Bảo đảm dự thầu (VND)', 'Hiệu lực của BĐDT (ngày)', 'Thời gian thực hiện hợp đồng']
    df_1_v4 = pd.DataFrame(columns=HSDXKT_columns_v4)

    HSDXKT_columns_v5 = ['Mã định danh', 'Tên nhà thầu', 'Hiệu lực E-HSĐXKT (ngày)', 'Thời gian thực hiện gói thầu']
    df_1_v5 = pd.DataFrame(columns=HSDXKT_columns_v5)
    HSDXKT_columns_v6 = ['Mã định danh', 'Tên nhà thầu', 'Hiệu lực E-HSDXKT (ngày)', 'Thời gian thực hiện gói thầu']
    df_1_v6 = pd.DataFrame(columns=HSDXKT_columns_v6)

    HSDXKT_columns_v7 = ["STT", "Mã định danh", "Tên nhà thầu", "Tên liên danh", "Hiệu lực HSĐXKT (ngày)", "Thời gian thực hiện gói thầu", "Giá trị của đảm bảo dự thầu", "Hiệu lực của đảm bảo dự thầu (ngày)"]
    df_1_v7 = pd.DataFrame(columns=HSDXKT_columns_v7)
    
    HSDXKT_columns_v8 = ['Mã định danh', 'Tên nhà thầu', 'Hiệu lực E-HSĐXKT (ngày)', 'Bảo đảm dự thầu (VND)', 'Hiệu lực của BĐDT (ngày)', 'Thời gian giao hàng']
    df_1_v8 = pd.DataFrame(columns=HSDXKT_columns_v8)
    HSDXKT_columns_v9 = ['Mã định danh', 'Tên nhà thầu', 'Hiệu lực E-HSDXKT (ngày)', 'Bảo đảm dự thầu (VND)', 'Hiệu lực của BĐDT (ngày)', 'Thời gian giao hàng']
    df_1_v9 = pd.DataFrame(columns=HSDXKT_columns_v9)

    DKT_columns_v1 = ['Mã định danh', 'Tên nhà thầu', 'Điểm kỹ thuật (nếu có)', 'Lý do chọn nhà thầu']
    df_2_v1 = pd.DataFrame(columns=DKT_columns_v1)
    DKT_columns_v2 = ['Mã định danh', 'Tên nhà thầu', 'Lý do chọn nhà thầu']
    df_2_v2 = pd.DataFrame(columns=DKT_columns_v2)
    DKT_columns_v3 = ['Mã định danh', 'Tên nhà thầu', 'Lý do không đáp ứng']
    df_2_v3 = pd.DataFrame(columns=DKT_columns_v3)

    data_1_v1 = []
    data_1_v2 = []
    data_1_v3 = []
    data_1_v4 = []
    data_1_v5 = []
    data_1_v6 = []
    data_1_v7 = []
    data_1_v8 = []
    data_1_v9 = []

    data_2_v1 = []
    data_2_v2 = []
    data_2_v3 = []

    df_all = pd.DataFrame()

    xpath_father = '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li'
    Box_info = driver.find_elements(By.XPATH, xpath_father)

    for i in range(len(Box_info)):
        box = driver.find_element(By.XPATH, f'{xpath_father}[{i+1}]')
        xpath_father_click = f'{xpath_father}[{i+1}]/a'
        if box.text == 'Biên bản mở E-HSDXKT' or box.text == 'Biên bản mở E-HSĐXKT' or box.text == 'Biên bản mở HSĐXKT' or box.text == 'Biên bản mở HSDXKT':
            click_wait(driver, xpath=xpath_father_click)
            print(f'Processing {box.text} {MA_TBMT}')
            wait_dual_data(driver, xpath_left='//*[@id="hsdxkt"]/div[1]/div[2]/div/div[1]', xpath_right='//*[@id="hsdxkt"]/div[1]/div[2]/div/div[2]')
            all_table = pd.read_html(StringIO(driver.page_source))
            for table in all_table:
                try:
                    if len(table.columns) == len(HSDXKT_columns_v1) and all(table.columns == HSDXKT_columns_v1):
                        data_1_v1 = table.values.tolist()
                        break
                    if len(table.columns) == len(HSDXKT_columns_v2) and all(table.columns == HSDXKT_columns_v2):
                        data_1_v2 = table.values.tolist()
                        break
                    if len(table.columns) == len(HSDXKT_columns_v3) and all(table.columns == HSDXKT_columns_v3):
                        data_1_v3 = table.values.tolist()
                        break
                    if len(table.columns) == len(HSDXKT_columns_v4) and all(table.columns == HSDXKT_columns_v4):
                        data_1_v4 = table.values.tolist()
                        break
                    if len(table.columns) == len(HSDXKT_columns_v5) and all(table.columns == HSDXKT_columns_v5):
                        data_1_v5 = table.values.tolist()
                        break
                    if len(table.columns) == len(HSDXKT_columns_v6) and all(table.columns == HSDXKT_columns_v6):
                        data_1_v6 = table.values.tolist()
                        break
                    if len(table.columns) == len(HSDXKT_columns_v7) and all(table.columns == HSDXKT_columns_v7):
                        data_1_v7 = table.values.tolist()
                        break
                    if len(table.columns) == len(HSDXKT_columns_v8) and all(table.columns == HSDXKT_columns_v8):
                        data_1_v8 = table.values.tolist()
                        break
                    if len(table.columns) == len(HSDXKT_columns_v9) and all(table.columns == HSDXKT_columns_v9):
                        data_1_v9 = table.values.tolist()
                        break
                except:
                    continue
            continue

        if box.text == 'Danh sách nhà thầu đạt kỹ thuật':
            click_wait(driver, xpath=xpath_father_click)
            print(f'Processing {box.text} {MA_TBMT}')
            wait_dual_data(driver, xpath_left='//*[@id="tab3"]/div[2]/div[2]/div/div[1]', xpath_right='//*[@id="tab3"]/div[2]/div[2]/div/div[2]')
            all_table = pd.read_html(StringIO(driver.page_source))
            for i, table in enumerate(all_table):
                try:
                    if len(table.columns) == len(DKT_columns_v1) and all(table.columns == DKT_columns_v1):
                        data_2_v1 = table.values.tolist()
                        break
                    if len(table.columns) == len(DKT_columns_v2) and all(table.columns == DKT_columns_v2):
                        data_2_v2 = table.values.tolist()
                        break
                    if len(table.columns) == len(DKT_columns_v3) and all(table.columns == DKT_columns_v3):
                        data_2_v3 = table.values.tolist()
                        break 
                except:
                    continue
            continue

    for i in range(len(data_1_v1)):
        df_1_v1.loc[i] = data_1_v1[i]
    for i in range(len(data_1_v2)):
        df_1_v2.loc[i] = data_1_v2[i]
    for i in range(len(data_1_v3)):
        df_1_v3.loc[i] = data_1_v3[i]
    for i in range(len(data_1_v4)):
        df_1_v4.loc[i] = data_1_v4[i]
    for i in range(len(data_1_v5)):
        df_1_v5.loc[i] = data_1_v5[i]
    for i in range(len(data_1_v6)):
        df_1_v6.loc[i] = data_1_v6[i]
    for i in range(len(data_1_v7)):
        df_1_v7.loc[i] = data_1_v7[i]
    for i in range(len(data_1_v8)):
        df_1_v8.loc[i] = data_1_v8[i]
    for i in range(len(data_1_v9)):
        df_1_v9.loc[i] = data_1_v9[i]

    for j in range(len(data_2_v1)):
        df_2_v1.loc[j] = data_2_v1[j]
    for j in range(len(data_2_v2)):
        df_2_v2.loc[j] = data_2_v2[j]
    for j in range(len(data_2_v3)):
        df_2_v3.loc[j] = data_2_v3[j]

    df_all = pd.concat([df_all, df_1_v1], ignore_index=True)
    df_all = pd.concat([df_all, df_1_v2], ignore_index=True)
    df_all = pd.concat([df_all, df_1_v3], ignore_index=True)
    df_all = pd.concat([df_all, df_1_v4], ignore_index=True)
    df_all = pd.concat([df_all, df_1_v5], ignore_index=True)
    df_all = pd.concat([df_all, df_1_v6], ignore_index=True)
    df_all = pd.concat([df_all, df_1_v7], ignore_index=True)
    df_all = pd.concat([df_all, df_1_v8], ignore_index=True)
    df_all = pd.concat([df_all, df_1_v9], ignore_index=True)
    
    df_all = pd.concat([df_all, df_2_v1], ignore_index=True)
    df_all = pd.concat([df_all, df_2_v2], ignore_index=True)
    df_all = pd.concat([df_all, df_2_v3], ignore_index=True)
    
    df_all['ly do'] = df_all['Lý do chọn nhà thầu'].combine_first(df_all['Lý do không đáp ứng'])
    

    rename_list = {
        'MaDinhDanh': [MaDinhDanh for _ in range(len(df_all))],
        'TenDonVi': [convert_MaDinhDanh_TenDonVi(MaDinhDanh) for _ in range(len(df_all))],
        'MA_TBMT': [MA_TBMT for _ in range(len(df_all))],
        'ID_TBMT': [ID_TBMT for _ in range(len(df_all))],
        'MADINHDANH': df_all['Mã định danh'].values,
        'TEN_NHATHAU': df_all['Tên nhà thầu'].values,
        'MA_LIENDANH': [None for _ in range(len(df_all))],
        'TEN_LIENDANH': [None for _ in range(len(df_all))],
        'LOAI_DANHGIA': [None for _ in range(len(df_all))],
        'KETQUA_DANHGIA': df_all['ly do'].values,
        'TECH_SCORE': df_all['Điểm kỹ thuật (nếu có)'].values
    }


    HSDXKT_DF = pd.DataFrame(rename_list)
    
    return HSDXKT_DF

    