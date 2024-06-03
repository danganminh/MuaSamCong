import pandas as pd
from io import StringIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def processing_LAM_RO(driver, TBMT, id_tbmt):

    print(f'Processing LAM_RO {TBMT}')

    id = []
    subjectCode = []
    catType = []
    ID_LAMRO = []
    YEUCAU_LAMRO_NGAY_KY = []
    YEUCAU_LAMRO_FILE_ID = []
    TRALOI_LAMRO_FILE_ID = []

    subjectName = []
    question = []
    response = []
    Ma_TBMT = []
    ID_TBMT = []
    YEUCAU_LAMRO_TEN = []
    YEUCAU_LAMRO_NGAY = []
    YEUCAU_LAMRO_FILE_NAME = []
    TRALOI_LAMRO_NGAY = []
    TRALOI_LAMRO_FILE_NAME = []

    columns = ['Mục cần làm rõ', 'Nội dung cần làm rõ', 'Nội dung trả lời']
    df = pd.DataFrame(columns=columns)
    data = []

    all_table = pd.read_html(StringIO(driver.page_source))
    index = 0
    for table in all_table:
        try:
            if len(table.columns) == len(columns) and all(table.columns == columns):
                df.loc[index] = table.values[0]
                index += 1
                break
        except:
            continue

    xpath_section = '//*[@id="clear-HSMT"]/div/div[2]/div/div/div/div[1]'
    box_section = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_section)))

    # Get value Lam Ro
    name_ = None
    time_ = None
    yeucau_lamro_ten = []
    yeucau_lamro_ngay = []
    for val in box_section:
        try:
            if len(yeucau_lamro_ten) == len(df): break
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
        except Exception as e:
            print(f'Error Get value Lam Ro in processing_LAM_RO as {str(e)}')
        finally:
            if len(yeucau_lamro_ten) != len(df):
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
        try:
            if len(yeucau_lamro_file_name) == len(df): break
            bottom = driver.find_elements(By.XPATH, f'//*[@id="clear-HSMT"]/div/div[2]/div/div/div[{i+2}]/div[2]/div/div')
            for i, val in enumerate(bottom):
                list_val_all = val.text.split(': ')
                if 'File đính kèm nội dung cần làm rõ' in val.text:
                    yeucau_lamro_file_name_elem = list_val_all[1]
                if 'File đính kèm nội dung trả lời' in val.text:
                    traloi_lamro_file_name_elem = list_val_all[1]
                if 'Ngày trả lời' in val.text:
                    traloi_lamro_ngay_elem = list_val_all[1]
        
        except Exception as e: 
            print(f'Error Get file_name_lam_ro in processing_LAM_RO as {str(e)}')
        
        finally:
            if len(yeucau_lamro_file_name) != len(df):
                yeucau_lamro_file_name.append(yeucau_lamro_file_name_elem)
                traloi_lamro_file_name.append(traloi_lamro_file_name_elem)
                traloi_lamro_ngay.append(traloi_lamro_ngay_elem)

                yeucau_lamro_file_name_elem = None
                traloi_lamro_file_name_elem = None
                traloi_lamro_ngay_elem = None
                

    # Append value
    subjectName.extend(df['Mục cần làm rõ'].values)
    question.extend(df['Nội dung cần làm rõ'].values)
    response.extend(df['Nội dung trả lời'].values)
    YEUCAU_LAMRO_TEN.extend(yeucau_lamro_ten)
    YEUCAU_LAMRO_NGAY.extend(yeucau_lamro_ngay)
    YEUCAU_LAMRO_FILE_NAME.extend(yeucau_lamro_file_name)
    TRALOI_LAMRO_NGAY.extend(traloi_lamro_ngay)
    TRALOI_LAMRO_FILE_NAME.extend(traloi_lamro_file_name)
    
    for _ in range(len(df)):
        Ma_TBMT.append(TBMT)
        ID_TBMT.append(id_tbmt)

        id.append(None)
        subjectCode.append(None)
        catType.append(None)
        ID_LAMRO.append(None)
        YEUCAU_LAMRO_NGAY_KY.append(None)
        YEUCAU_LAMRO_FILE_ID.append(None)
        TRALOI_LAMRO_FILE_ID.append(None)


    data = {
        'id': id,
        'subjectCode': subjectCode,
        'subjectName': subjectName,
        'question': question,
        'response': response,
        'catType': catType,
        'ID_LAMRO': ID_LAMRO,
        'Ma_TBMT': Ma_TBMT,
        'ID_TBMT': ID_TBMT,
        'YEUCAU_LAMRO_TEN': YEUCAU_LAMRO_TEN,
        'YEUCAU_LAMRO_NGAY': [val if val else None for val in YEUCAU_LAMRO_NGAY],
        'YEUCAU_LAMRO_NGAY_KY': YEUCAU_LAMRO_NGAY_KY,
        'YEUCAU_LAMRO_FILE_ID': YEUCAU_LAMRO_FILE_ID,
        'YEUCAU_LAMRO_FILE_NAME': YEUCAU_LAMRO_FILE_NAME,
        'TRALOI_LAMRO_NGAY': [val if val else None for val in TRALOI_LAMRO_NGAY],
        'TRALOI_LAMRO_FILE_ID': TRALOI_LAMRO_FILE_ID,
        'TRALOI_LAMRO_FILE_NAME': TRALOI_LAMRO_FILE_NAME
    }
    
    
    LAM_RO = pd.DataFrame(data)

    return LAM_RO
