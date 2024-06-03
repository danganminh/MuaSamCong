import time
import warnings
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from functions.func_model_1.GOI_THAU import processing_GOI_THAU
from functions.func_model_1.GOI_THAU_CT import processing_GOI_THAU_CT
from functions.func_model_1.KHLCNT import processing_KHLCNT
from functions.func_model_1.LAM_RO import processing_LAM_RO
from functions.func_model_1.KIEN_NGHI import processing_Kien_Nghi
from functions.func_model_1.BIENBAN_MOTHAU import processing_BienBanMoThau
from functions.func_model_1.HSDXKT import processing_HSDXKT
from functions.func_model_1.HSDXTC import processing_HSDXTC
from functions.func_model_1.KQChonNhaThau import processing_KQChonThau

import locale
from functions.logic import short_link
from GoogleSheet_Works import *
from send_mess import *
from functions.logic import *

warnings.simplefilter(action='ignore', category=FutureWarning)

home_page = 'https://muasamcong.mpi.gov.vn'

def check_banner(driver):
    try:
        wait_load(driver, xpath='//*[@id="notification-popup-v2"]/div/div/div/div/p', key='THÔNG BÁO QUAN TRỌNG')
        close_button = driver.find_element(By.XPATH, '//*[@id="popup-close"]')
        close_button.click()
        print('Banner Closed')
    except:
        print('Banner not found or unable to close.')


def get_keys_to_search_homepage(driver, key):
    try:
        # Click clear Box
        wait_load(driver, xpath='//*[@id="home"]/div/div/div/div', key='Tìm kiếm thông tin đấu thầu', refresh=True)
        #KHLCNT_button
        driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[3]/div[1]/div[2]/label[1]/span').click()
        time.sleep(1)
        #ChuDauTu_botton
        driver.find_element(By.XPATH, '//*[@id="checkbox-4"]').click()
        time.sleep(1)
        Input_text = driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/input')
        if key:
            Input_text.clear()
            time.sleep(1)
            Input_text.send_keys(key)
            time.sleep(1)
            #search_button
            driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/button').click()
    except Exception as e:
        print(f'Error in get_keys_to_search_homepage: {str(e)}')


# Crawl value in result page
def get_value_box(driver, index):    
    link = driver.find_element(By.XPATH, f'//*[@id="bid-closed"]/div[{index}]/div/div[2]/div[1]/a').get_attribute('href')
    PL_code = link.split("planNo=")[1].split("&")[0]
    return link, PL_code


def get_info_new_value(driver, KHLCNT_code):
    # Convert to string, because Can't check duplication String with Int
    KHLCNT_code = [str(val) if val else None for val in KHLCNT_code]
    link_new, PL_new = [], []
    try:
        while True:
            # Add 50 result/page
            wait_load(driver, xpath='//*[@id="search-home"]/div/div/div/div/div/label', key='kết quả', refresh=True)
            # fifty
            options = driver.find_elements(By.XPATH, '//*[@id="search-home"]/div/div[3]/div[1]/div[3]/div[2]/select/option')
            for op in options:
                if op.text == '50':
                    op.click()
                    time.sleep(1)
            wait_load(driver, xpath='//*[@id="bid-closed"]/div', key='Mã KHLCNT', refresh=True)
            Results_Box = driver.find_elements(By.XPATH, '//*[@id="bid-closed"]/div')
            for i in range(len(Results_Box)):
                link, PL_code = get_value_box(driver, index=i+1)
                if PL_code not in KHLCNT_code and PL_code not in PL_new:
                    link_new.append(link)
                    PL_new.append(PL_code)
            try: # Click next page                       
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-home"]/div/div[3]/div[2]/div/div/button[2]'))).click()
            except TimeoutException:
                break
    except Exception as e:
        print(f"Error get_info_new_value as {str(e)}")
    finally:
        return link_new, PL_new


def get_link_PL_MaDinhDanh(driver, data_base, MAPPING_TENDONVI_KEYS):

    KHLCNT_code = data_base['planNo'].values
    keys = MAPPING_TENDONVI_KEYS
    link_ar = []
    PL_code_ar = []
    MaDinhDanh_ar = []
    first = True
    for key in keys:
        if not key: break
        driver.get(home_page)
        if first:
            check_banner(driver)
            first = False
        #get_keys_to_search(driver, key)
        get_keys_to_search_homepage(driver, key)
        link, PL_code = get_info_new_value(driver, KHLCNT_code)
        print(key, PL_code)
        for l, p in zip(link, PL_code):
            # skip link tbmt
            if 'stepCode=notify-contractor-step-1-tbmt' in l.split('&'): continue
            if p not in PL_code_ar:
                link_ar.append(l)
                PL_code_ar.append(p)
                MaDinhDanh_ar.append(key)
    
    return link_ar, PL_code_ar, MaDinhDanh_ar


def Step_1_module_1(driver, plan, madinhdanh):

    KHLCNT_temp = pd.DataFrame()
    GOI_THAU_temp = pd.DataFrame()

    # START
    driver.get(home_page)
    wait_load(driver, xpath='//*[@id="home"]/div/div/div/div', key='Tìm kiếm thông tin đấu thầu', refresh=True)
    # Click on the label to select the planNo option
    planNo_label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[3]/div[1]/div[2]/label[1]/span'))
    )
    planNo_label.click()
    time.sleep(1)
    planNo_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/input'))
    )
    planNo_input.clear()
    time.sleep(1)
    planNo_input.send_keys(plan)
    time.sleep(1)
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/button'))
    )
    search_button.click()
    
    # Get the link result of planNo
    wait_load(driver, xpath='//*[@id="search-home"]/div/div/div/div/div/label', key='kết quả', refresh=True)
    link_detail = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]/a')
    driver.get(link_detail.get_attribute('href'))

    KHLCNT_temp = processing_KHLCNT(driver, plan, madinhdanh)
    GOI_THAU_temp = processing_GOI_THAU(driver, plan, madinhdanh)

    return KHLCNT_temp, GOI_THAU_temp 


def Step_2_module_1(driver, TBMT, id_tbmt):

    LAM_RO_temp = pd.DataFrame()
    KIEN_NGHI_temp = pd.DataFrame()    
    
    driver.get(home_page)
    wait_load(driver, xpath='//*[@id="home"]/div/div/div/div', key='Tìm kiếm thông tin đấu thầu', refresh=True)
    # Input TBMT to search page
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/input'))
    )
    search_input.clear()
    time.sleep(1)
    search_input.send_keys(TBMT)
    time.sleep(1)
    # Click on the label for selecting the search option
    label_TBMT = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/label[1]/span'))
    )
    label_TBMT.click()
    time.sleep(1)
    # Click on the search button
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/button'))
    )
    search_button.click()
    wait_load(driver, xpath='//*[@id="search-home"]/div/div/div/div/div/label', key='kết quả', refresh=True)
    link_detail = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]/a')
    TITLE_TBMT = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]/a/h5').text
    driver.get(link_detail.get_attribute('href'))
    wait_load(driver, xpath='//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div/h5', key=TITLE_TBMT, refresh=True)

    xpath_child = '//*[@id="tenderNotice"]/ul/li'
    box_child_sec = driver.find_elements(By.XPATH, xpath_child)
    for i in range(len(box_child_sec)):
        child_section = driver.find_element(By.XPATH, f'{xpath_child}[{i+1}]')
        xpath_child_click = f'{xpath_child}[{i+1}]'
        if child_section.text == 'Làm rõ HSMT':
            click_wait(driver, xpath=xpath_child_click)
            check_value = driver.find_element(By.XPATH, '//*[@id="clear-HSMT"]/div/div/div').text
            if 'Không có nội dung' not in check_value:
                LAM_RO_temp = processing_LAM_RO(driver, TBMT, id_tbmt)
                if LAM_RO_temp.empty:
                    print(f'Empty LAM_RO {TBMT}')
                    
        elif child_section.text == 'Kiến nghị':
            click_wait(driver, xpath=xpath_child_click)
            check_value = driver.find_element(By.XPATH, '//*[@id="kien-nghi"]/div/div/div').text
            if 'Không có nội dung kiến nghị' not in check_value:
                KIEN_NGHI_temp = processing_Kien_Nghi(driver, TBMT)
                if KIEN_NGHI_temp.empty:
                    print(f'Empty KIEN_NGHI {TBMT}')

    return LAM_RO_temp, KIEN_NGHI_temp


def Step_3_module_1(driver, data_base_with_TBMT, index):
    
    GOI_THAU_CT_temp = pd.DataFrame()
    GIA_HAN_temp = pd.DataFrame()

    GOI_THAU_CT_temp, GIA_HAN_temp = processing_GOI_THAU_CT(driver, data_base_with_TBMT, index)

    return GOI_THAU_CT_temp, GIA_HAN_temp


def Step_4_module_1(driver, TBMT, id_tbmt):
    
    BIENBAM_MOTHAU_temp = pd.DataFrame()
    HSDXTC_temp = pd.DataFrame()
    KQLCNT_temp = pd.DataFrame()

    xpath_father = '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li'
    Box_info = driver.find_elements(By.XPATH, xpath_father)
    for i in range(len(Box_info)):
        box = driver.find_element(By.XPATH, f'{xpath_father}[{i+1}]')
        xpath_father_click = f'{xpath_father}[{i+1}]/a'
        if box.text == 'Biên bản mở thầu':
            click_wait(driver, xpath=xpath_father_click)
            wait_load(driver, xpath='//*[@id="bidOpeningMinutes"]/div[1]/div', key='Biên bản mở thầu')
            BIENBAM_MOTHAU_temp = processing_BienBanMoThau(driver, TBMT, id_tbmt)
            if BIENBAM_MOTHAU_temp.empty:
                print(f'Empty BIENBAM_MOTHAU {TBMT}')
            
        if box.text == 'Biên bản mở E-HSDXTC' or box.text == 'Biên bản mở E-HSĐXTC' or box.text == 'Biên bản mở HSDXTC' or box.text == 'Biên bản mở HSĐXTC':
            click_wait(driver, xpath=xpath_father_click)
            wait_load(driver, xpath='//*[@id="hsdxtc"]/div[1]/div', key='Biên bản mở thầu')
            HSDXTC_temp = processing_HSDXTC(driver, TBMT, id_tbmt)
            if HSDXTC_temp.empty:
                print(f'Empty HSDXTC {TBMT}')
                
        if box.text == 'Kết quả lựa chọn nhà thầu':
            click_wait(driver, xpath=xpath_father_click)
            wait_load(driver, xpath='//*[@id="contractorSelectionResults"]/div[1]/div', key='Thông tin gói thầu')
            KQLCNT_temp = processing_KQChonThau(driver, TBMT, id_tbmt) 
            if KQLCNT_temp.empty:
                print(f'Empty KQLCNT {TBMT}')
                
    return BIENBAM_MOTHAU_temp, HSDXTC_temp, KQLCNT_temp


def Step_5_module_1(driver, TBMT, id_tbmt, MaDinhDanh):
    
    HSDXKT_temp = pd.DataFrame()
    # processing_HSDXKT if have Biên bản mở E-HSDXKT then have Danh sách nhà thầu đạt kỹ thuật
    wait_load(driver, xpath='//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li', key='Thông báo mời thầu')
    HSDXKT_temp = processing_HSDXKT(driver, TBMT, id_tbmt, MaDinhDanh)
    if HSDXKT_temp.empty:
        print(f'Empty HSDXKT {TBMT}')
    return HSDXKT_temp


# Function to format TBMT message
def TBMT_new(df):
    locale.setlocale(locale.LC_ALL, '')
    url_short = short_link(df['LINK'])
    temp = f"""
🆕 TBMT MỚI 🌟

- Đơn vị: {df['TenDonVi']}
- Mã TBMT: {df['MA_TBMT']}
- Tên gói thầu: {df['TEN_GOITHAU']}
- Ngày đăng tải: {df['NGAYDANGTAI_TBMT']}
- Giá gói thầu: {locale.format_string("%d", df['GIA_GOITHAU'], grouping=True).replace('.', ',')} {df['CCY_GIA_GOITHAU']}
- Thời điểm mở thầu: {df['THOIDIEM_MOTHAU']}
- Thời điểm đóng thầu: {df['THOIDIEM_DONGTHAU']}
- QĐ phê duyệt HSMT: {df['HSMT_SOQD']} ({df['HSMT_NGAYQD']})
- Link: {url_short}"""
    return temp

# Function to format KHLCNT message
def KHLCNT_new(df):
    url_short = short_link(df['LINK'])
    temp = f"""
🆕 KHLCNT MỚI 🌟

- Đơn vị: {df['TenDonVi']}
- Mã KHLCNT: {df['planNo']}
- Tên KHLCNT: {df['planName']}
- Ngày đăng tải: {df['NgayDangTai_KHLCNT']}
- Số lượng gói thầu: {df['SoLuongGoiThau']}
- QĐ phê duyệt: {df['QD_KHLCNT_So']} ({df['QD_KHLCNT_Ngay']}) 
- Link: {url_short}"""
    return temp


def module_1(driver, data_base, MAPPING_TENDONVI_KEYS):

    KHLCNT = pd.DataFrame()
    GOI_THAU = pd.DataFrame()
    GOI_THAU_CT = pd.DataFrame()
    LAM_RO = pd.DataFrame()
    GIA_HAN = pd.DataFrame()
    KIEN_NGHI = pd.DataFrame()
    BIENBAN_MOTHAU = pd.DataFrame()
    HSDXKT = pd.DataFrame()
    HSDXTC = pd.DataFrame()
    KQLCNT = pd.DataFrame()

    _, PL_code_ar, MaDinhDanh_ar = get_link_PL_MaDinhDanh(driver, data_base, MAPPING_TENDONVI_KEYS)
    driver.get(home_page)
    count = 0
    for plan, madinhdanh in zip(PL_code_ar, MaDinhDanh_ar):
        try:
            #if count == 1: break
            count += 1
            # Step 1
            KHLCNT_temp, GOI_THAU_temp = Step_1_module_1(driver, plan, madinhdanh)
            if not GOI_THAU_temp.empty:
                data_base_with_TBMT = GOI_THAU_temp.dropna(subset=['MA_TBMT']).reset_index(drop=True)
                for index, (TBMT, id_tbmt) in enumerate(zip(data_base_with_TBMT['MA_TBMT'].values, data_base_with_TBMT['ID_TBMT'].values)):
            # Step 2
                    LAM_RO_temp, KIEN_NGHI_temp = Step_2_module_1(driver, TBMT, id_tbmt)
            # Step 3
                    GOI_THAU_CT_temp, GIA_HAN_temp = Step_3_module_1(driver, data_base_with_TBMT, index)
            # Step 4
                    BIENBAM_MOTHAU_temp, HSDXTC_temp, KQLCNT_temp = Step_4_module_1(driver, TBMT, id_tbmt)
            # Step 5
                    HSDXKT_temp = Step_5_module_1(driver, TBMT, id_tbmt, madinhdanh)

                # APPEND DATA WHEN DONE
                    LAM_RO = pd.concat([LAM_RO, LAM_RO_temp], ignore_index=True)
                    KIEN_NGHI = pd.concat([KIEN_NGHI, KIEN_NGHI_temp], ignore_index=True)
                    GOI_THAU_CT = pd.concat([GOI_THAU_CT, GOI_THAU_CT_temp], ignore_index=True)
                    GIA_HAN = pd.concat([GIA_HAN, GIA_HAN_temp], ignore_index=True)
                    BIENBAN_MOTHAU = pd.concat([BIENBAN_MOTHAU, BIENBAM_MOTHAU_temp], ignore_index=True)
                    HSDXTC = pd.concat([HSDXTC, HSDXTC_temp], ignore_index=True)
                    KQLCNT = pd.concat([KQLCNT, KQLCNT_temp], ignore_index=True)
                    HSDXKT = pd.concat([HSDXKT, HSDXKT_temp], ignore_index=True)
            
            KHLCNT = pd.concat([KHLCNT, KHLCNT_temp], ignore_index=True)
            GOI_THAU = pd.concat([GOI_THAU, GOI_THAU_temp], ignore_index=True)
            
        except Exception as e:
            print(f'Error main module_1 plan: {plan, madinhdanh} as {str(e)}')
            continue            
    
    # Send mess to telegram
    KHLCNT_MESS = [KHLCNT_new(KHLCNT.iloc[i]) for i in range(len(KHLCNT))]
    TBMT_MESS = [TBMT_new(GOI_THAU_CT.iloc[i]) for i in range(len(GOI_THAU_CT))]
        
    return KHLCNT, GOI_THAU, GOI_THAU_CT, GIA_HAN, LAM_RO, KIEN_NGHI, BIENBAN_MOTHAU, HSDXKT, HSDXTC, KQLCNT, KHLCNT_MESS, TBMT_MESS