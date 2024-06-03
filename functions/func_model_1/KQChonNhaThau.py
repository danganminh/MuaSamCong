import pandas as pd
from io import StringIO
from selenium.webdriver.common.by import By

from functions.logic import get_value, convert_str_to_dtype, wait_dual_data

def get_value_ngaykethopdong(driver):
    columns = ["STT", "Nhà thầu", "Ngày ký hợp đồng"]
    result = pd.DataFrame(columns=columns)
    data = []
    all_table = pd.read_html(StringIO(driver.page_source))
    for table in all_table:
        try:
            if len(table.columns) == len(columns) and all(table.columns == columns):
                data = table.values.tolist()
                break
        except:
            continue
    
    for i in range(len(data)):
        result.loc[i] = data[i]

    return result


def processing_KQChonThau(driver, MA_TBMT, ID_TBMT, NgayDangTai_SQDPD=False):

    print(f'Processing KQChonThau {MA_TBMT}')

    columns_1 = ['STT', 'Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Giá trúng thầu (VND)', 'Thời gian thực hiện hợp đồng']
    df_1 = pd.DataFrame(columns=columns_1)
    columns_2 = ["STT", "Mã định danh", "Tên nhà thầu", "Giá dự thầu (VND)", "Giá trúng thầu (VND)", "Thời gian giao hàng", "Thời gian giao hàng chi tiết"]
    df_2 = pd.DataFrame(columns=columns_2)
    columns_6 = ['STT', 'Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Điểm kỹ thuật (nếu có)', 'Giá trúng thầu (VND)', 'Thời gian thực hiện hợp đồng']
    df_6 = pd.DataFrame(columns=columns_6)
    columns_3 = ["STT","Mã định danh","Tên nhà thầu","Tên liên danh","Giá dự thầu (VND)","Điểm kỹ thuật (nếu có)","Giá trúng thầu (VND)","Thời gian thực hiện hợp đồng","Thời gian thực hiện hợp đồng chi tiết"]
    df_3 = pd.DataFrame(columns=columns_3)
    columns_4 = ['STT', 'Mã định danh', 'Tên nhà thầu', 'Tên liên danh', 'Giá dự thầu (VND)', 'Giá trúng thầu (VND)', 'Thời gian giao hàng', 'Thời gian giao hàng chi tiết']
    df_4 = pd.DataFrame(columns=columns_4)

    # Nha thau khong duoc chon
    columns_5 = ['STT', 'Mã định danh', 'Tên nhà thầu', 'Lý do không được lựa chọn của từng nhà thầu']
    df_5 = pd.DataFrame(columns=columns_5)

    columns_7= ["STT","Mã định danh","Mã số thuế","Tên nhà thầu","Giá dự thầu (VND)","Giá trúng thầu (VND)","Thời gian thực hiện gói thầu","Thời gian thực hiện gói thầu chi tiết","Thời gian thực hiện hợp đồng"]
    df_7 = pd.DataFrame(columns=columns_7)

    columns_8 = ["STT", "Mã định danh", "Tên nhà thầu", "Giá dự thầu (VND)", "Giá trúng thầu (VND)", "Thời gian thực hiện hợp đồng", "Thời gian thực hiện hợp đồng chi tiết"]
    df_8 = pd.DataFrame(columns=columns_8)
    
    df_all = pd.DataFrame()
    
    data_1 = []
    data_2 = []
    data_6 = []
    data_3 = []
    data_4 = []
    data_5 = []
    data_7 = []
    data_8 = []

    wait_dual_data(driver, xpath_left='//*[@id="contractorSelectionResults"]/div[1]/div[2]/div/div[1]', xpath_right='//*[@id="contractorSelectionResults"]/div[1]/div[2]/div/div[2]')
    # Nha thau duoc chon
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
            if len(table.columns) == len(columns_6) and all(table.columns == columns_6):
                data_6 = table.values.tolist()
                break
            if len(table.columns) == len(columns_7) and all(table.columns == columns_7):
                data_7 = table.values.tolist()
                break
            if len(table.columns) == len(columns_8) and all(table.columns == columns_8):
                data_8 = table.values.tolist()
                break
        except:
            continue

    # Nha thau khong chung thau
    for table in all_table:
        try:
            if len(table.columns) == len(columns_5) and all(table.columns == columns_5):
                data_5 = table.values.tolist()
                break
        except:
            continue

    tengoithau = get_value(driver, key='Tên gói thầu', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
    bidResult = get_value(driver, key='Phiên bản thay đổi', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
    if bidResult and '\n' in bidResult:
        bidResult = bidResult.split('\n')[-1]
    lotPrice = get_value(driver, key='Giá gói thầu', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
    

    for i in range(len(data_1)):
        df_1.loc[i] = data_1[i]
    for i in range(len(data_2)):
        df_2.loc[i] = data_2[i]
    for i in range(len(data_6)):
        df_6.loc[i] = data_6[i]
    for i in range(len(data_3)):
        df_3.loc[i] = data_3[i]
    for i in range(len(data_4)):
        df_4.loc[i] = data_4[i]
    for i in range(len(data_5)):
        df_5.loc[i] = data_5[i]
    for i in range(len(data_7)):
        df_7.loc[i] = data_7[i]
    for i in range(len(data_8)):
        df_8.loc[i] = data_8[i]

    df_all = pd.concat([df_all, df_1], ignore_index=True)
    df_all = pd.concat([df_all, df_2], ignore_index=True)
    df_all = pd.concat([df_all, df_6], ignore_index=True)
    df_all = pd.concat([df_all, df_3], ignore_index=True)
    df_all = pd.concat([df_all, df_4], ignore_index=True)
    df_all = pd.concat([df_all, df_5], ignore_index=True)
    df_all = pd.concat([df_all, df_7], ignore_index=True)
    df_all = pd.concat([df_all, df_8], ignore_index=True)

    ngayky = get_value_ngaykethopdong(driver)
    ngayky_hopdong = []
    for madinhdanh in df_all['Mã định danh'].values:
        try:
            have_value = False
            for nha_thau, ngay_ky in zip(ngayky['Nhà thầu'].values, ngayky['Ngày ký hợp đồng'].values):
                if madinhdanh == nha_thau:
                    ngayky_hopdong.append(ngay_ky)
                    have_value = True
                    break
            if not have_value:
                ngayky_hopdong.append(None)
        except:
            ngayky_hopdong.append(None)
            continue

    df_all['tengoithau'] = [tengoithau for _ in range(len(df_all))]
    df_all['ngayky'] = [val for val in ngayky_hopdong]
    df_all['bidResult'] = [bidResult for _ in range(len(df_all))]
    df_all['lotPrice'] = [lotPrice for _ in range(len(df_all))]

    # Convert data type
    df_all['Giá dự thầu (VND)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df_all['Giá dự thầu (VND)'].values]
    df_all['Giá trúng thầu (VND)'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df_all['Giá trúng thầu (VND)'].values]
    df_all['lotPrice'] = [convert_str_to_dtype(val, float)[0] if val else None for val in df_all['lotPrice'].values]
    
    rename_list = {
        'id': [None for _ in range(len(df_all))],
        'Ma_TBMT': [MA_TBMT for _ in range(len(df_all))],
        'ID_TBMT': [ID_TBMT for _ in range(len(df_all))],
        'lotNo': [None for _ in range(len(df_all))],
        'lotName': df_all['tengoithau'].values,
        'ventureCode': [None for _ in range(len(df_all))],
        'ventureName': df_all['Tên liên danh'].values,
        'orgCode': df_all['Mã định danh'].values,
        'orgFullname': df_all['Tên nhà thầu'].values,
        'bidWiningPrice': df_all['Giá trúng thầu (VND)'].values,
        'reason': df_all['Lý do không được lựa chọn của từng nhà thầu'].values,
        'bidResult': df_all['bidResult'].values,
        'role': [None for _ in range(len(df_all))],
        'evalBidPrice': [None for _ in range(len(df_all))],
        'lotPrice': df_all['lotPrice'].values,
        'lotFinalPrice': df_all['Giá dự thầu (VND)'].values,
        'discountPercent': [None for _ in range(len(df_all))],
        'techScore': [None for _ in range(len(df_all))],
        'recEmail': [None for _ in range(len(df_all))],
        'taxCode': [None for _ in range(len(df_all))],
        'cperiodText': df_all['Thời gian thực hiện hợp đồng'].values,
        'contractSignDate': [val if val else None for val in df_all['ngayky'].values]
    }

    KQChonThau = pd.DataFrame(rename_list)
    
    if NgayDangTai_SQDPD:
        try:
            hh_mm = driver.find_element(By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[2]/div/div[1]/p[2]').text
            dd_mm_yyyy = driver.find_element(By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[2]/div/div[1]/p[3]').text
            ngay_dang_tai = f'{dd_mm_yyyy} {hh_mm}'
        except:
            ngay_dang_tai = None
            
        sqdpd = get_value(driver, key='Số quyết định phê duyệt', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
        ngay_pd = get_value(driver, key='Ngày phê duyệt', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
        
        return KQChonThau, ngay_dang_tai, sqdpd, ngay_pd
    
    return KQChonThau