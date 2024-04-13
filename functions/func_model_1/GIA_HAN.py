import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def processing_GIA_HAN(driver, data_base, index):

    GIA_HAN_DF = pd.DataFrame()

    columns = ['MA_TBMT', 'STT', 'Thời điểm gia hạn thành công', 'Thời điểm đóng thầu cũ', 'Thời điểm đóng thầu sau gia hạn', 'Thời điểm mở thầu cũ', 'Thời điểm mở thầu sau gia hạn', 'Lý do']
    table = pd.DataFrame(columns=columns)
    data = []
    have_value = False

    #ID_GIAHAN = []
    #TAIKHOAN_GIAHAN = []

    try:

        xpath_section = '//*[@id="info-general"]/div/div[1]'
        box_section = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, xpath_section)))
        for i in range(len(box_section)):
            if 'Thông tin gia hạn' in box_section[i].text:
                have_value = True
                xpath_tbody = f'//*[@id="info-general"]/div[{i+2}]/div[2]/table'
                try:
                    tbody = driver.find_element(By.XPATH, xpath_tbody)
                    for tr in tbody.find_elements(By.XPATH, '//tr'):
                        row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                        if row and len(row) != 0:
                            ma_tbmt = data_base['MA_TBMT'].iloc[index].copy()
                            ma_tbmt.extend(row)
                            data.append(ma_tbmt)
                    break
                except:
                    continue

        if have_value == False:
            print('None Gia_Han')
        else:
            for i in range(len(data)):
                table.loc[i] = data[i]

            GIA_HAN_DF = pd.DataFrame({
                'MA_TBMT': table['MA_TBMT'].to_list(),
                'LAN_GIAHAN': table['STT'].to_list(),
                'THOIDIEM_MOTHAU_CU': table['Thời điểm mở thầu cũ'].to_list(),
                'THOIDIEM_DONGTHAU_CU': table['Thời điểm đóng thầu cũ'].to_list(),
                'THOIDIEM_MOTHAU_MOI': table['Thời điểm mở thầu sau gia hạn'].to_list(),
                'THOIDIEM_DONGTHAU_MOI': table['Thời điểm đóng thầu sau gia hạn'].to_list(),
                'LYDO': table['Lý do'].to_list()
            })

    except Exception as e:
        print(f'Error processing_GIA_HAN as {str(e)} ')
    
    finally:
        return GIA_HAN_DF