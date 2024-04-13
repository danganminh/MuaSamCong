import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def processing_Kien_Nghi(driver, TBMT):

    #petitionPeriod = []
    #isDecision = []
    #reason = []
    reqContent = []
    resContent = []
    #reqDate = []
    #resDate = []
    reqFileName = []
    #reqFileId = []
    resFileName = []
    #resFileId = []
    #ID_KIENNGHI = []
    #MA_KIENNGHI = []
    TEN_KIENNGHI = []
    #NGAY_KIENNGHI = []
    #MA_DINHDANH_NHATHAU_KIENNGHI = []
    #NHATHAU_KIENNGHI = []
    #STATUS = []
    MA_TBMT = []
    ID_TBMT = []
    
    try:
        columns = ['STT', 'Loại kiến nghị', 'Tên kiến nghị', 'Nội dung kiến nghị']
        df_temp = pd.DataFrame(columns=columns)

        box = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="kien-nghi"]/div/div[2]')))

        data = []
        for i in range(len(box)):
            if 'Phiên bản :' in box[i].text:
                xpath_tbody = f'//*[@id="kien-nghi"]/div/div[2]/div/table' #/tbody'
                tbody = driver.find_element(By.XPATH, xpath_tbody)
                temp = None
                for tr in tbody.find_elements(By.XPATH, '//tr'):
                    row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                    if 0 < len(row) < 7:
                        #for col in df.columns.reverse():
                        if row[0] == 'STT':
                            continue # skip columns
                        if len(row) == 4:  
                            data.append(row)
                        elif len(row) == 2:
                            if temp:
                                STT_val = temp[0]
                                TENKIENNGHI_val = temp[2]
                            data.append([STT_val, row[0], TENKIENNGHI_val, row[1]])
                    temp = row
                break

        for i in range(len(data)):
            df_temp.loc[i] = data[i]

        stt = df_temp['STT'].value_counts().keys()

        reqContent_val = []
        resContent_val = []
        reqFileName_val = []
        resFileName_val = []
        tenkiennghi_val = []
        for s in stt:
            data_temp = df_temp.where(df_temp['STT'] == s).dropna().reset_index(drop=True)
            index = 0
            for noidung in data_temp['Nội dung kiến nghị'].values:
                if 'Nội dung kiến nghị :' in noidung:
                    reqContent_val.append(noidung.split('Nội dung kiến nghị :')[1].split('\n')[0].strip())
                else:
                    reqContent_val.append(None)
                if 'Nội dung trả lời :' in noidung:
                    resContent_val.append(noidung.split('Nội dung trả lời :')[1].split('\n')[0].strip())
                else:
                    resContent_val.append(None)
                if 'File đính kèm nội dung kiến nghị :' in noidung:
                    reqFileName_val.append(noidung.split('File đính kèm nội dung kiến nghị :')[1].split('\n')[0].strip())
                else:
                    reqFileName_val.append(None)
                if 'File đính kèm nội dung trả lời :' in noidung:
                    resFileName_val.append(noidung.split('File đính kèm nội dung trả lời :')[1].split('\n')[0].strip())
                else:
                    resFileName_val.append(None)
                tenkiennghi_val.append(data_temp['Tên kiến nghị'].iloc[[index]])
                index += 1
        
        reqContent.extend(reqContent_val)
        resContent.extend(resContent_val)
        reqFileName.extend(reqFileName_val)
        resFileName.extend(resFileName_val)
        TEN_KIENNGHI.extend(tenkiennghi_val)
        for _ in range(len(reqContent)):
            MA_TBMT.append(TBMT)
            ID_TBMT.append(driver.current_url.split('&id=')[1].split('&')[0])

    except Exception as e:
        print(f'Error processing_Kien_Nghi as {str(e)}')


    data = {
        # 'petitionPeriod': petitionPeriod,
        # 'isDecision': isDecision,
        # 'reason': reason,
        'reqContent': reqContent,
        'resContent': resContent,
        # 'reqDate': reqDate,
        # 'resDate': resDate,
        'reqFileName': reqFileName,
        # 'reqFileId': reqFileId,
        'resFileName': resFileName,
        # 'resFileId': resFileId,
        # 'ID_KIENNGHI': ID_KIENNGHI,
        # 'MA_KIENNGHI': MA_KIENNGHI,
        'TEN_KIENNGHI': TEN_KIENNGHI,
        #'NGAY_KIENNGHI': NGAY_KIENNGHI,
        # 'MA_DINHDANH_NHATHAU_KIENNGHI': MA_DINHDANH_NHATHAU_KIENNGHI,
        # 'NHATHAU_KIENNGHI': NHATHAU_KIENNGHI,
        # 'STATUS': STATUS,
        'MA_TBMT': MA_TBMT,
        'ID_TBMT': ID_TBMT
    }

    # Print the length of each list
    print("\nLength of each list using for DEBUG KIEN_NGHI:")
    for name, lst in data.items():
        print(f"{name}: {len(lst)}")

    df = pd.DataFrame(data)

    return df