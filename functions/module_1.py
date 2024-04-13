import time
import warnings
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from functions.func_model_1.GOI_THAU import prcessing_GOI_THAU
from functions.func_model_1.GOI_THAU_CT import prcessing_GOI_THAU_CT
from functions.func_model_1.KHLCNT import prcessing_KHLCNT
from functions.func_model_1.LAM_RO import processing_LAM_RO
from functions.func_model_1.KIEN_NGHI import processing_Kien_Nghi
from functions.func_model_1.BIENBAN_MOTHAU import processing_BienBanMoThau
from functions.func_model_1.HSDXKT import processing_HSDXKT
from functions.func_model_1.HSDXTC import processing_HSDXTC
from functions.func_model_1.KQChonNhaThau import processing_KQChonThau

from functions.logic import wait_load, click_element

warnings.simplefilter(action='ignore', category=FutureWarning)

home_page = 'https://muasamcong.mpi.gov.vn'
search_page = 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?render=search'


def check_banner(driver):
    try:
        wait_load(driver, xpath='//*[@id="notification-popup-v2"]/div/div/div/div/p', key='THÔNG BÁO QUAN TRỌNG')
        close_button = driver.find_element(By.XPATH, '//*[@id="popup-close"]')
        close_button.click()
        print('Banner Closed')
    except:
        print('Banner not found or unable to close.')

# Import code to search page
def get_keys_to_search(driver, key):
    try:
        # Click clear Box
        time.sleep(5)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-advantage-haunt"]/div/div/div/div/div/div[3]/button[1]'))).click()
        ChuDauTu_Box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="search-advantage-haunt"]/div/div/div/div/div/div[2]/div[7]/div[2]/div/div[1]/input')))
        if key is not None:
            ChuDauTu_Box.send_keys(key)
            add_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-advantage-haunt"]/div/div/div/div/div/div[2]/div[7]/div[2]/div/div[2]/button')))
            add_button.click()
            search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-advantage-haunt"]/div/div/div/div/div/div[3]/button[2]')))
            search_button.click()
    except Exception as e:
        print(f'Error in get_keys_to_search: {str(e)}')

def get_keys_to_search_homepage(driver, key):
    try:
        # Click clear Box
        wait_load(driver, xpath='//*[@id="home"]/div/div/div/div', key='Tìm kiếm thông tin đấu thầu')
        #KHLCNT_button
        driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[3]/div[1]/div[2]/label[1]/span').click()
        #ChuDauTu_botton
        driver.find_element(By.XPATH, '//*[@id="checkbox-4"]').click()
        Input_text = driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/input')
        if key is not None:
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
    link_new = []
    PL_new = []
    try:
        while True:
            # Add 50 result/page
            wait_load(driver, xpath='//*[@id="search-home"]/div/div/div/div/div/label', key='kết quả')
            # fifty
            options = driver.find_elements(By.XPATH, '//*[@id="search-home"]/div/div[3]/div[1]/div[3]/div[2]/select/option')
            for op in options:
                if op.text == '50':
                    op.click()
                    time.sleep(3)
            wait_load(driver, xpath='//*[@id="bid-closed"]/div', key='Mã KHLCNT')
            Results_Box = driver.find_elements(By.XPATH, '//*[@id="bid-closed"]/div')
            for i in range(len(Results_Box)):
                link, PL_code = get_value_box(driver, index=i+1)
                if PL_code not in KHLCNT_code and PL_code not in PL_new:
                    link_new.append(link)
                    PL_new.append(PL_code)
            try: # Click next page                       
                WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search-home"]/div/div[3]/div[2]/div/div/button[2]'))).click()
            except Exception:
                break
    except Exception as e:
        print(f"Error get_info_new_value as {str(e)}")
    finally:
        return link_new, PL_new


def get_link_PL_MaDinhDanh(driver, data_base, MAPPING_TENDONVI):

    KHLCNT_code = pd.read_excel(data_base, sheet_name='2.1.KHLCNT')['planNo'].values
    keys = MAPPING_TENDONVI.keys()
    link_ar = []
    PL_code_ar = []
    MaDinhDanh_ar = []
    # Search all value with MaDinhDanh
    link_ar = []
    PL_code_ar = []
    MaDinhDanh_ar = []
    first = True
    # Get All PL_code
    #count = 1
    for key in keys:
        if not key:
            break
    #    if count > 2:
    #        break
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
            if 'stepCode=notify-contractor-step-1-tbmt' in l.split('&'):
                continue
            if l not in link_ar:       
                link_ar.append(l)
                PL_code_ar.append(p)
                MaDinhDanh_ar.append(key)
    #    count +=1
    
    return link_ar, PL_code_ar, MaDinhDanh_ar


def module_1(driver, data_base, MAPPING_TENDONVI):

    KHLCNT = pd.DataFrame()
    GOI_THAU = pd.DataFrame()
    LAM_RO = pd.DataFrame()
    GIA_HAN = pd.DataFrame()
    KIEN_NGHI = pd.DataFrame()
    GOI_THAU_CT = pd.DataFrame()
    BIENBAM_MOTHAU = pd.DataFrame()
    HSDXKT = pd.DataFrame()
    HSDXTC = pd.DataFrame()
    KQLCNT = pd.DataFrame()

    link_ar, PL_code_ar, MaDinhDanh_ar = get_link_PL_MaDinhDanh(driver, data_base, MAPPING_TENDONVI)
    
    #first = True
    for plan, madinhdanh, link in zip(PL_code_ar, MaDinhDanh_ar, link_ar):
        try:
            #======== PROCESSING KHLCNT PAGE #========
            driver.get(home_page)
            wait_load(driver, xpath='//*[@id="home"]/div/div/div/div', key='Tìm kiếm thông tin đấu thầu')
            # if first:
            #     check_banner(driver, time=10)
            #     first = False
            # Click on the label to select the planNo option
            planNo_label = driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[3]/div[1]/div[2]/label[1]/span')
            planNo_label.click()
            # Input the planNo to the search box
            planNo_input = driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/input')
            planNo_input.send_keys(plan)
            # Click on the search button
            search_button = driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/button')
            search_button.click()
            # Get the link result of planNo
            wait_load(driver, xpath='//*[@id="search-home"]/div/div/div/div/div/label', key='kết quả')
            link_detail = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]/a')
            driver.get(link_detail.get_attribute('href'))
            
            print('\nStart prcessing_KHLCNT')
            KHLCNT_temp = prcessing_KHLCNT(driver, plan, madinhdanh, link)

            print('\nStart prcessing_GOI_THAU')
            GOI_THAU_temp = prcessing_GOI_THAU(driver, plan, madinhdanh, link)


            #======== PROCESSING TBMT PAGE #========
            data_base_with_TBMT = GOI_THAU_temp.copy()
            data_base_with_TBMT = data_base_with_TBMT.dropna(subset=['MA_TBMT']).reset_index(drop=True)
            index = 0
            for TBMT, id_tbmt in zip(data_base_with_TBMT['MA_TBMT'].values, data_base_with_TBMT['ID_TBMT'].values):
                print(f'\n----- Processing {TBMT} -----')
                driver.get(home_page)
                wait_load(driver, xpath='//*[@id="home"]/div/div/div/div', key='Tìm kiếm thông tin đấu thầu')
                # Input TBMT to search page
                search_input = driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/input')
                search_input.clear()
                time.sleep(1)
                search_input.send_keys(TBMT)
                time.sleep(1)
                # Click on the label for selecting the search option
                label_TBMT = driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/label[1]/span')
                label_TBMT.click()
                time.sleep(1)
                # Click on the search button
                search_button = driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/button')
                search_button.click()
                wait_load(driver, xpath='//*[@id="search-home"]/div/div/div/div/div/label', key='kết quả')
                link_detail = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]/a')
                TITLE_TBMT = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]/a/h5').text
                
                driver.get(link_detail.get_attribute('href'))
                wait_load(driver, xpath='//*[@id="tender-notice"]/div/div/div/div/div/div/div', key=TITLE_TBMT)
                SAVE_LINK = driver.current_url

                # PROCESSING CHILD SECTION IN "Thông báo mời thầu"
                box_child_sec = driver.find_elements(By.XPATH, '//*[@id="tenderNotice"]/ul/li')
                for i in range(len(box_child_sec)):
                    xpath_child_sec = f'//*[@id="tenderNotice"]/ul/li[{i+1}]/a'
                    child_sec = driver.find_element(By.XPATH, xpath_child_sec)
                    if child_sec.text == 'Làm rõ HSMT':
                        click_element(child_sec)
                        wait_load(driver, xpath='//*[@id="clear-HSMT"]/div/div', key='Thông tin làm rõ')
                        check_value = driver.find_element(By.XPATH, '//*[@id="clear-HSMT"]/div/div/div').text
                        if 'Không có nội dung' not in check_value:
                            wait_load(driver, xpath='//*[@id="clear-HSMT"]/div/div[2]/div/div/div[2]/div', key='Tên yêu cầu')
                            LAM_RO_temp = processing_LAM_RO(driver, TBMT, id_tbmt)
                            if not LAM_RO_temp.empty:
                                LAM_RO = pd.concat([LAM_RO, LAM_RO_temp], ignore_index=True)
                        else:
                            print('None LAM_RO')
                    if child_sec.text == 'Kiến nghị':
                        click_element(child_sec)
                        wait_load(driver, xpath='//*[@id="kien-nghi"]/div/div', key='Kiến nghị')                                                          
                        check_value = driver.find_element(By.XPATH, '//*[@id="kien-nghi"]/div/div/div').text
                        if 'Không có nội dung kiến nghị' not in check_value:
                            wait_load(driver, xpath='//*[@id="kien-nghi"]/div/div[2]/div/div/span', key='Phiên bản')
                            KIEN_NGHI_temp = processing_Kien_Nghi(driver, TBMT)
                            if not KIEN_NGHI_temp.empty:
                                KIEN_NGHI = pd.concat([KIEN_NGHI, KIEN_NGHI_temp], ignore_index=True)
                        else:
                            print('None KIEN NGHI')
                    break
                
                print('\nStart prcessing_GOI_THAU_CT')
                GOI_THAU_CT_temp, GIA_HAN_temp = prcessing_GOI_THAU_CT(driver, data_base_with_TBMT, index)
                
                if not GOI_THAU_CT_temp.empty:
                    GOI_THAU_CT = pd.concat([GOI_THAU_CT, GOI_THAU_CT_temp], ignore_index=True)
                if not GIA_HAN_temp.empty:
                    GIA_HAN = pd.concat([GIA_HAN, GIA_HAN_temp], ignore_index=True)


                driver.get(SAVE_LINK)
                wait_load(driver, xpath='//*[@id="tender-notice"]/div/div/div/div/div/div/div', key=TITLE_TBMT)

                # Father tree
                xpath_father = '//*[@id="tender-notice"]/div/div/div/div/div/div/div/ul/li'
                box_father = driver.find_elements(By.XPATH, xpath_father)
                for box in box_father:
                    if box.text == 'Biên bản mở thầu':
                        click_element(box.find_element(By.XPATH, ".//a"))
                        wait_load(driver, xpath='//*[@id="bidOpeningMinutes"]/div[1]/div', key='Biên bản mở thầu')
                        BIENBAM_MOTHAU_temp = processing_BienBanMoThau(driver, TBMT, id_tbmt)
                        if not BIENBAM_MOTHAU_temp.empty:
                            BIENBAM_MOTHAU = pd.concat([BIENBAM_MOTHAU, BIENBAM_MOTHAU_temp], ignore_index=True)

                    if box.text == 'Biên bản mở E-HSDXTC':
                        click_element(box.find_element(By.XPATH, ".//a"))
                        wait_load(driver, xpath='//*[@id="hsdxtc"]/div[1]/div', key='Biên bản mở thầu')
                        HSDXTC_temp = processing_HSDXTC(driver, TBMT, id_tbmt)
                        if not HSDXTC_temp.empty:
                            HSDXTC = pd.concat([HSDXTC, HSDXTC_temp], ignore_index=True)

                    if box.text == 'Kết quả lựa chọn nhà thầu':
                        click_element(box.find_element(By.XPATH, ".//a"))
                        wait_load(driver, xpath='//*[@id="contractorSelectionResults"]/div[1]/div', key='Thông tin gói thầu')
                        KQLCNT_temp = processing_KQChonThau(driver, TBMT, id_tbmt)
                        if not KQLCNT_temp.empty:
                            KQLCNT = pd.concat([KQLCNT, KQLCNT_temp], ignore_index=True)
                    
                    if box.text == 'Biên bản mở E-HSDXKT':
                        # processing_HSDXKT if have Biên bản mở E-HSDXKT then have Danh sách nhà thầu đạt kỹ thuật
                        HSDXKT_temp = processing_HSDXKT(driver, TBMT, id_tbmt)
                        if not HSDXKT_temp.empty:
                            HSDXKT = pd.concat([HSDXKT, HSDXKT_temp], ignore_index=True)

                index += 1

            if not GOI_THAU_temp.empty:
                GOI_THAU = pd.concat([GOI_THAU, GOI_THAU_temp], ignore_index=True)
            if not KHLCNT_temp.empty:
                KHLCNT = pd.concat([KHLCNT, KHLCNT_temp], ignore_index=True)
            

        except Exception as e:
            print(f'Error as {str(e)}')
            continue

    return GOI_THAU, GOI_THAU_CT, KHLCNT, LAM_RO, KIEN_NGHI, GIA_HAN, BIENBAM_MOTHAU, HSDXKT, HSDXTC, KQLCNT