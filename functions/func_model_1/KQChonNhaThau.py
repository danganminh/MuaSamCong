import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functions.logic import get_value, convert_str_to_dtype

def get_value_ngaykethopdong(driver):
    columns = ["STT", "Nhà thầu", "Ngày ký hợp đồng"]
    result = pd.DataFrame(columns=columns)
    data = []
    try:
        section = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="contractorSelectionResults"]/div/div[1]')))
        for i, sec in enumerate(section):
            if sec.text == 'Thông tin ký kết hợp đồng':
                xpath_table = f'//*[@id="contractorSelectionResults"]/div[{i+1}]/div[2]/div/table' 
                try:
                    tbody = driver.find_element(By.XPATH, xpath_table)
                    for tr in tbody.find_elements(By.XPATH, '//tr'):
                        row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                        if row[0] != '':
                            data.append(row)
                    break
                except:
                    continue
        
        for i in range(len(data)):
            result.loc[i] = data[i]

    except Exception as e:
        print(f'Error get_value_ngaykethopdong as {str(e)}')

    finally:
        if not result.empty:
            return result['Ngày ký hợp đồng'].dropna().values
        else:
            return None


def processing_KQChonThau(driver, MA_TBMT, ID_TBMT):

    columns_1 = ['Ma_TBMT', 'ID_TBMT', 'STT', 'Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Giá trúng thầu (VND)', 'Thời gian thực hiện hợp đồng']
    df_1 = pd.DataFrame(columns=columns_1)
    columns_2 = ['Ma_TBMT', 'ID_TBMT', "STT", "Mã định danh", "Tên nhà thầu", "Giá dự thầu (VND)", "Giá trúng thầu (VND)", "Thời gian giao hàng", "Thời gian giao hàng chi tiết"]
    df_2 = pd.DataFrame(columns=columns_2)
    KQChonThau = pd.DataFrame()
    data_1 = []
    data_2 = []

    try:
        section = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="contractorSelectionResults"]/div/div[1]')))
        for i, sec in enumerate(section):
            if sec.text == 'Thông tin Nhà thầu trúng thầu':
                xpath_table = f'//*[@id="contractorSelectionResults"]/div[{i+1}]/div[2]/table'
                try:
                    tbody = driver.find_element(By.XPATH, xpath_table)
                    for tr in tbody.find_elements(By.XPATH, '//tr'):
                        row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                        value = [MA_TBMT, ID_TBMT]
                        value.extend(row)
                        if len(row) == len(columns_1) - 2:
                            data_1.append(value)
                        elif len(row) == len(columns_2) - 2:
                            data_2.append(value)
                    break
                except:
                    continue
        
        tengoithau = get_value(driver, key='Tên gói thầu', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
        bidResult = get_value(driver, key='Phiên bản thay đổi', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
        lotPrice = get_value(driver, key='Giá gói thầu', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')

        if data_1:
            for i in range(len(data_1)):
                df_1.loc[i] = data_1[i]
        if data_2:
            for j in range(len(data_2)):
                df_2.loc[j] = data_2[j]
        
        KQChonThau = pd.concat([df_1, df_2], ignore_index=True)

        KQChonThau['tengoithau'] = [tengoithau for _ in range(len(KQChonThau))]
        KQChonThau['ngayky'] = get_value_ngaykethopdong(driver)
        KQChonThau['bidResult'] = [bidResult for _ in range(len(KQChonThau))]
        KQChonThau['lotPrice'] = [lotPrice for _ in range(len(KQChonThau))]

        KQChonThau = KQChonThau.rename(columns={
            "Mã định danh": "orgCode",
            "Tên nhà thầu": "orgFullname",
            "tengoithau": "lotName",
            "Giá trúng thầu (VND)": "bidWiningPrice",
            "Giá dự thầu (VND)": "lotFinalPrice",
            "Thời gian thực hiện hợp đồng": "cperiodText",
            "ngayky": "contractSignDate)"
        })

        # Convert data type
        KQChonThau['lotFinalPrice'] = [convert_str_to_dtype(val, float)[0] if val else None for val in KQChonThau['lotFinalPrice'].values]
        KQChonThau['bidWiningPrice'] = [convert_str_to_dtype(val, float)[0] if val else None for val in KQChonThau['bidWiningPrice'].values]
        KQChonThau['lotPrice'] = [convert_str_to_dtype(val, float)[0] if val else None for val in KQChonThau['lotPrice'].values]

        # Drop STT
        KQChonThau = KQChonThau.drop(labels=['STT'],axis=1)

    except Exception as e:
        print(f'Error processing_KQChonThau as {str(e)}')

    finally:
        return KQChonThau
