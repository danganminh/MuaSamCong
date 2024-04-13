import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from functions.logic import wait_load, click_element

def processing_HSDXKT(driver, MA_TBMT, ID_TBMT):

    HSDXKT_columns = ['MA_TBMT', 'ID_TBMT', 'Mã định danh', 'Tên nhà thầu', 'Hiệu lực HSDXKT (ngày)', 'Thời gian thực hiện hợp đồng']
    df_1 = pd.DataFrame(columns=HSDXKT_columns)
    DKT_columns_v1 = ['MA_TBMT', 'ID_TBMT', 'Mã định danh', 'Tên nhà thầu', 'Điểm kỹ thuật (nếu có)', 'Lý do chọn nhà thầu']
    df_2_v1 = pd.DataFrame(columns=DKT_columns_v1)
    DKT_columns_v2 = ['MA_TBMT', 'ID_TBMT', 'Mã định danh', 'Tên nhà thầu', 'Lý do chọn nhà thầu']
    df_2_v2 = pd.DataFrame(columns=DKT_columns_v2)

    xpath_box = '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li'
    box_father = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath_box)))

    data_1 = []
    data_2_v1 = []
    data_2_v2 = []

    HSDXKT_DF = pd.DataFrame()

    try:
        for i, box in enumerate(box_father):
            if box.text == 'Biên bản mở E-HSDXKT':
                click_element(driver.find_element(By.XPATH, f'{xpath_box}[{i+1}]/a'))
                wait_load(driver, xpath='//*[@id="hsdxkt"]/div[1]/div', key='Biên bản mở thầu')
                xpath_section = '//*[@id="hsdxkt"]/div/div[1]'
                section = driver.find_elements(By.XPATH, xpath_section)
                for j, sec in enumerate(section):
                    if sec.text == 'Thông tin nhà thầu':
                        xpath_table = f'//*[@id="hsdxkt"]/div[{j+1}]/div[2]/div/table'
                        try:
                            tbody = driver.find_element(By.XPATH, xpath_table)
                            for tr in tbody.find_elements(By.XPATH, '//tr'):
                                row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                                value = [MA_TBMT, ID_TBMT]
                                value.extend(row)
                                if len(row) == len(HSDXKT_columns) - 2:
                                    data_1.append(value)
                            break
                        except:
                            continue

            if box.text == 'Danh sách nhà thầu đạt kỹ thuật':
                click_element(driver.find_element(By.XPATH, f'{xpath_box}[{i+1}]/a'))
                wait_load(driver, xpath='//*[@id="tab3"]/div[1]/div', key='Thông tin gói thầu')
                xpath_section = '//*[@id="tab3"]/div/div[1]'
                section = driver.find_elements(By.XPATH, xpath_section)
                for j, sec in enumerate(section):
                    if sec.text == 'Thông tin các nhà thầu đáp ứng yêu cầu về kỹ thuật':
                        xpath_table = f'//*[@id="tab3"]/div[{j+1}]/div[3]/table'
                        try:
                            tbody = driver.find_element(By.XPATH, xpath_table)
                            for tr in tbody.find_elements(By.XPATH, '//tr'):
                                row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                                value = [MA_TBMT, ID_TBMT]
                                value.extend(row)
                                if len(row) == len(DKT_columns_v1) - 2:
                                    data_2_v1.append(value)
                                elif len(row) == len(DKT_columns_v2) - 2:
                                    data_2_v2.append(value)
                            break
                        except:
                            continue

        for i in range(len(data_1)):
            df_1.loc[i] = data_1[i]

        for j in range(len(data_2_v1)):
            df_2_v1.loc[j] = data_2_v1[j]
        
        for k in range(len(data_2_v2)):
            df_2_v2.loc[k] = data_2_v2[k]

        HSDXKT_DF = pd.concat([df_1, df_2_v1], ignore_index=True)
        HSDXKT_DF = pd.concat([HSDXKT_DF, df_2_v2], ignore_index=True)

        HSDXKT_DF = HSDXKT_DF.rename(columns={
            "Mã định danh": "MADINHDANH", 
            "Tên nhà thầu": "TEN_NHATHAU",
            "Lý do chọn nhà thầu": "LOAI_DANHGIA",
            "Điểm kỹ thuật (nếu có)": "TECH_SCORE"
        })

    except Exception as e:
        print(f'Error processing_HSDXKT {str(e)}')
    
    finally:
        return HSDXKT_DF

    