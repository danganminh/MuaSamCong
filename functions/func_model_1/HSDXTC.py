import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functions.logic import convert_str_to_dtype

def processing_HSDXTC(driver, MA_TBMT, ID_TBMT):

    columns = ['Ma_TBMT', 'ID_TBMT', 'Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (VND)', 'Điểm kỹ thuật', 'Hiệu lực E-HSĐXTC (ngày)']
    HSDXTC = pd.DataFrame(columns=columns)
    data = []
    
    try:
        section = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="hsdxtc"]/div/div[1]')))
        for i, sec in enumerate(section):
            if sec.text == 'Thông tin nhà thầu':
                xpath_table = f'//*[@id="hsdxtc"]/div[{i+1}]/div[2]/table'
                try:
                    tbody = driver.find_element(By.XPATH, xpath_table)
                    for tr in tbody.find_elements(By.XPATH, '//tr'):
                        row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                        if len(row) >= 7:
                            if row[0] != '':
                                ma_tbmt = [MA_TBMT, ID_TBMT]
                                ma_tbmt.extend(row)
                                data.append(ma_tbmt)
                    break
                except:
                    continue

        for i in range(len(data)):
            HSDXTC.loc[i] = data[i]
        
        HSDXTC = HSDXTC.rename(columns={
            "Mã định danh": "contractorCode_final",
            "Tên nhà thầu": "contractorName_final",
            "Giá dự thầu (VND)": "bidPrice",
            "Tỷ lệ giảm giá (%)": "saleNumber",
            "Giá dự thầu sau giảm giá (VND)": "bidFinalPrice",
            "Điểm kỹ thuật": "techScore",
            "Hiệu lực E-HSĐXTC (ngày)": "NewContractPeriod (Day)"
        })

        # Convert data type
        HSDXTC['bidPrice'] = [convert_str_to_dtype(val, float)[0] if val else None for val in HSDXTC['bidPrice'].values]
        HSDXTC['saleNumber'] = [convert_str_to_dtype(val, float)[0] if val else None for val in HSDXTC['saleNumber'].values]
        HSDXTC['bidFinalPrice'] = [convert_str_to_dtype(val, float)[0] if val else None for val in HSDXTC['bidFinalPrice'].values]
        HSDXTC['techScore'] = [convert_str_to_dtype(val, float)[0] if val else None for val in HSDXTC['techScore'].values]
        HSDXTC['NewContractPeriod'] = [convert_str_to_dtype(val, float)[0] if val else None for val in HSDXTC['NewContractPeriod (Day)'].values]

    except Exception as e:
        print(f'Error processing_HSDXTC as {str(e)}')

    finally:
        return HSDXTC