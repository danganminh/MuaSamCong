import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def processing_BienBanMoThau(driver, MA_TBMT, ID_TBMT):

    columns_1 = ['MA_TBMT', 'ID_TBMT', 'Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (nếu có) (VND)', 'Hiệu lực báo giá (ngày)', 'Thời gian giao hàng']
    df_1 = pd.DataFrame(columns=columns_1)

    columns_2 = ['MA_TBMT', 'ID_TBMT', 'Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Tỷ lệ giảm giá (%)', 'Giá dự thầu sau giảm giá (nếu có) (VND)', 'Hiệu lực E-HSDT (ngày)', 'Giá trị bảo đảm dự thầu (VND)', 'Hiệu lực bảo đảm dự thầu (ngày)', 'Thời gian thực hiện hợp đồng']
    df_2 = pd.DataFrame(columns=columns_2)

    BIENBAN_MOTHAU_DF = pd.DataFrame()
    data = []

    try:
        xpath_section = '//*[@id="bidOpeningMinutes"]/div/div[1]' 
        box_section = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath_section)))
        for i in range(len(box_section)):
            if 'Thông tin nhà thầu' in box_section[i].text:
                xpath_tbody = f'//*[@id="bidOpeningMinutes"]/div[{i+1}]/div[2]/table' #/tbody' //*[@id="bidOpeningMinutes"]/div[2]/div[2]/table
                try:
                    tbody = driver.find_element(By.XPATH, xpath_tbody)
                    for tr in tbody.find_elements(By.XPATH, '//tr'):
                        row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                        if row and len(row) >= len(columns_1) - 2:
                            value = [MA_TBMT, ID_TBMT]
                            value.extend(row)
                            data.append(value)
                    break
                except:
                    continue
        
        count_1 = 0
        count_2 = 0
        for i in range(len(data)):
            if len(data[i]) == len(columns_1):
                df_1.loc[count_1] = data[i]
                count_1 += 1
            else:
                df_2.loc[count_2] = data[i]
                count_2 += 1

        BIENBAN_MOTHAU_DF = pd.concat([df_1, df_2], ignore_index=True)

    except Exception as e:
        print(f'Error processing_BienBanMoThau as {str(e)}')
    
    finally:
        return BIENBAN_MOTHAU_DF







