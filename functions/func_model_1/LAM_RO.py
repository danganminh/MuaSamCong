import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def processing_LAM_RO(driver, TBMT, id_tbmt):

    #id = []
    #subjectCode = []
    subjectName = []
    question = []
    response = []
    #catType = []
    #ID_LAMRO = []
    Ma_TBMT = []
    ID_TBMT = []
    YEUCAU_LAMRO_TEN = []
    YEUCAU_LAMRO_NGAY = []
    #YEUCAU_LAMRO_NGAY_KY = []
    #YEUCAU_LAMRO_FILE_ID = []
    YEUCAU_LAMRO_FILE_NAME = []
    TRALOI_LAMRO_NGAY = []
    #TRALOI_LAMRO_FILE_ID = []
    TRALOI_LAMRO_FILE_NAME = []

    try:
        xpath_section = '//*[@id="clear-HSMT"]/div/div[2]/div/div/div[2]/div[1]'
        box_section = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_section)))
        columns = ['Mục cần làm rõ', 'Nội dung cần làm rõ', 'Nội dung trả lời']
        table = pd.DataFrame(columns=columns)
        data = []
        for i in range(len(box_section)):
            xpath_table = f'//*[@id="clear-HSMT"]/div/div[2]/div/div/div[{i+2}]/div[2]/div[2]/table/tbody'
            try:
                count = 1
                tbody = driver.find_element(By.XPATH, xpath_table)
                for tr in tbody.find_elements(By.XPATH, '//tr'):
                    if count > 1:
                        break
                    row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                    if len(row) >= 3:
                        if row[0] != '':
                            data.append(row)
                            count += 1
                            break
            except:
                continue
        
        for i in range(len(data)):
            table.loc[i] = data[i]

        # # Get value Lam Ro
        name_ = None
        time_ = None
        yeucau_lamro_ten = []
        yeucau_lamro_ngay = []
        for val in box_section:
            list_val_all = val.text.split(': ')
            for i, list_val in enumerate(list_val_all):
                if 'Tên yêu cầu làm rõ' in list_val:
                    ten = list_val_all[i+1]
                    if '\n' in ten:
                        ten = ten.split('\n')[0]
                    else:
                        ten = ten
                    name_ = ten
                if 'Ngày gửi yêu cầu' in list_val:
                    ngay = list_val_all[i+1]
                    time_ = ngay
            yeucau_lamro_ten.append(name_)
            yeucau_lamro_ngay.append(time_)
            name_ = None
            time_ = None


        # Get file_name_lam_ro
        yeucau_lamro_file_name = []
        yeucau_lamro_file_name_elem = None

        traloi_lamro_file_name = []
        traloi_lamro_file_name_elem = None

        traloi_lamro_ngay = []
        traloi_lamro_ngay_elem = None

        for i in range(len(box_section)):
            bottom = driver.find_elements(By.XPATH, f'//*[@id="clear-HSMT"]/div/div[2]/div/div/div[{i+2}]/div[2]/div/div')
            for i, val in enumerate(bottom):
                list_val_all = val.text.split(': ')
                if 'File đính kèm nội dung cần làm rõ' in val.text:
                    yeucau_lamro_file_name_elem = list_val_all[1]
                if 'File đính kèm nội dung trả lời' in val.text:
                    traloi_lamro_file_name_elem = list_val_all[1]
                if 'Ngày trả lời' in val.text:
                    traloi_lamro_ngay_elem = list_val_all[1]
            yeucau_lamro_file_name.append(yeucau_lamro_file_name_elem)
            traloi_lamro_file_name.append(traloi_lamro_file_name_elem)
            traloi_lamro_ngay.append(traloi_lamro_ngay_elem)

            yeucau_lamro_file_name_elem = None
            traloi_lamro_file_name_elem = None
            traloi_lamro_ngay_elem = None

        # Append value
        subjectName.extend(table['Mục cần làm rõ'].values)
        question.extend(table['Nội dung cần làm rõ'].values)
        response.extend(table['Nội dung trả lời'].values)
        YEUCAU_LAMRO_TEN.extend(yeucau_lamro_ten)
        YEUCAU_LAMRO_NGAY.extend(yeucau_lamro_ngay)
        YEUCAU_LAMRO_FILE_NAME.extend(yeucau_lamro_file_name)
        TRALOI_LAMRO_NGAY.extend(traloi_lamro_ngay)
        TRALOI_LAMRO_FILE_NAME.extend(traloi_lamro_file_name)
        for _ in range(len(table)):
            Ma_TBMT.append(TBMT)
            ID_TBMT.append(id_tbmt)

    except Exception as e:
        print(f'Error processing_LAM_RO as {str(e)}')


    data = {
        #'id': id,
        #'subjectCode': subjectCode,
        'subjectName': subjectName,
        'question': question,
        'response': response,
        #'catType': catType,
        #'ID_LAMRO': ID_LAMRO,
        'Ma_TBMT': Ma_TBMT,
        'ID_TBMT': ID_TBMT,
        'YEUCAU_LAMRO_TEN': YEUCAU_LAMRO_TEN,
        'YEUCAU_LAMRO_NGAY': YEUCAU_LAMRO_NGAY,
        #'YEUCAU_LAMRO_NGAY_KY': YEUCAU_LAMRO_NGAY_KY,
        #'YEUCAU_LAMRO_FILE_ID': YEUCAU_LAMRO_FILE_ID,
        'YEUCAU_LAMRO_FILE_NAME': YEUCAU_LAMRO_FILE_NAME,
        'TRALOI_LAMRO_NGAY': TRALOI_LAMRO_NGAY,
        #'TRALOI_LAMRO_FILE_ID': TRALOI_LAMRO_FILE_ID,
        'TRALOI_LAMRO_FILE_NAME': TRALOI_LAMRO_FILE_NAME
    }

    # Print the length of each list
    print("\nLength of each list using for DEBUG LAM_RO:")
    for name, lst in data.items():
        print(f"{name}: {len(lst)}")

    df = pd.DataFrame(data)

    return df