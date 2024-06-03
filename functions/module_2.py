import time
import locale
import warnings
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from functions.func_model_1.GOI_THAU import processing_GOI_THAU_Update_module2, processing_MaTBMT
from functions.func_model_1.GOI_THAU_CT import processing_GOI_THAU_CT
from functions.func_model_1.BIENBAN_MOTHAU import processing_BienBanMoThau
from functions.func_model_1.HSDXKT import processing_HSDXKT
from functions.func_model_1.HSDXTC import processing_HSDXTC
from functions.func_model_1.KQChonNhaThau import processing_KQChonThau

from functions.func_model_1.LAM_RO import processing_LAM_RO
from functions.func_model_1.KIEN_NGHI import processing_Kien_Nghi

from functions.my_driver import custom_driver
from functions.logic import *

warnings.simplefilter(action='ignore', category=FutureWarning)


home_page = 'https://muasamcong.mpi.gov.vn'


def search_TBMT(driver, TBMT):
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
    
    link = link_detail.get_attribute('href')
    STT = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[1]/span').text    
    TITLE = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]/a/h5').text
    
    return link, STT, TITLE


def check_banner(driver):
    try:
        wait_load(driver, xpath='//*[@id="notification-popup-v2"]/div/div/div/div/p', key='THÔNG BÁO QUAN TRỌNG')
        close_button = driver.find_element(By.XPATH, '//*[@id="popup-close"]')
        close_button.click()
        print('Banner Closed')
    except:
        print('Banner not found or unable to close.')
        

def Step_1_Update_TBMT(driver, GOI_THAU):
    
    GOI_THAU_NEW = pd.DataFrame()
    GOI_THAU_CT_NEW = pd.DataFrame()
    GIA_HAN_NEW = pd.DataFrame()
        
    index_null_TBMT = GOI_THAU[GOI_THAU['MAPPING_STATUS_TBMT'] == "01. Chưa có TBMT"].index.tolist()
    first = True

    planNo = GOI_THAU['planNo'].values[index_null_TBMT]
    planNo_Not_Duplicate = []

    all_tengoithau = []
    all_ma_tbmt = []
    
    count = 0
    for plan, index in zip(planNo, index_null_TBMT):
        # Skip Duplicate
        if plan not in planNo_Not_Duplicate:
            planNo_Not_Duplicate.append(plan)
        else:
            continue
        
        #if count >= 10: break
        count += 1
        
        driver.get(home_page)
        if first:
            check_banner(driver)
            first = False
            
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

        # Click ThongTinGoiThau
        click_wait(driver, xpath='//*[@id="tender-notice"]/div/div/div[1]/div[1]/div[2]/ul/li[2]/a')
        wait_dual_data(driver, xpath_left='//*[@id="tab2"]/div[2]/div[2]/div/div[1]', xpath_right='//*[@id="tab2"]/div[2]/div[2]/div/div[2]')

        tengoithau, gia_goithau, ma_tbmt = processing_MaTBMT(driver)
        all_tengoithau.append(tengoithau)
        all_ma_tbmt.append(ma_tbmt)
    
    # Create pandas with values tengoithau, ma_tbmt
    all_TBMT = pd.DataFrame({
        "tengoithau": all_tengoithau,
        "IB": all_ma_tbmt
    })
    
    # Search new values by TEN_GOITHAU
    TenGoiThau_old = GOI_THAU['TEN_GOITHAU'].values[index_null_TBMT]
    
    search_data = all_TBMT[all_TBMT['tengoithau'].isin(TenGoiThau_old)]
    search_data = search_data.dropna(subset=['IB']).reset_index(drop=True)
    
    MA_TBMT = search_data['IB'].values
    index_new = GOI_THAU[GOI_THAU['TEN_GOITHAU'].isin(all_TBMT['tengoithau'])].index.tolist()
    MA_TBMT_Not_Duplicate = []
    
    # search_TBMT
    for tbmt, index in zip(MA_TBMT, index_new):
        # Skip Duplicate
        if tbmt not in MA_TBMT_Not_Duplicate:
            MA_TBMT_Not_Duplicate.append(tbmt)
        else:
            continue
        
        driver.get(home_page)
        wait_load(driver, xpath='//*[@id="home"]/div/div/div/div', key='Tìm kiếm thông tin đấu thầu', refresh=True)
        # Click on the label
        TBMT_method = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/label[1]/span'))
        )
        TBMT_method.click()
        time.sleep(1)
        TBMT_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/input'))
        )
        TBMT_input.clear()
        time.sleep(1)
        TBMT_input.send_keys(tbmt)
        time.sleep(1)
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/button'))
        )
        search_button.click()
    
        wait_load(driver, xpath='//*[@id="search-home"]/div/div/div/div/div/label', key='kết quả', refresh=True)        
        # Check if dont have TBMT, skip 
        try:        
            link_detail = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]/a')
            STT = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[1]/span').text
            driver.get(link_detail.get_attribute('href'))
            print(f'New TBMT: {tbmt}')
        except NoSuchElementException:
            print(f'None new TBMT: {tbmt}')
            continue
        
        # Get new data GOI_THAU
        GOI_THAU_temp = processing_GOI_THAU_Update_module2(driver, STT, GOI_THAU, index)
        # Get new data GOI_THAU_CT
        GOI_THAU_CT_NEW_temp, GIA_HAN_NEW_temp = processing_GOI_THAU_CT(driver, GOI_THAU_temp, 0)
        
        GOI_THAU_NEW = pd.concat([GOI_THAU_NEW, GOI_THAU_temp], ignore_index=True)
        GOI_THAU_CT_NEW = pd.concat([GOI_THAU_CT_NEW, GOI_THAU_CT_NEW_temp], ignore_index=True)
        GIA_HAN_NEW = pd.concat([GIA_HAN_NEW, GIA_HAN_NEW_temp], ignore_index=True)
                
    return GOI_THAU_NEW, GOI_THAU_CT_NEW, GIA_HAN_NEW


def Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW):
    
    LAM_RO_NEW = pd.DataFrame()
    KIEN_NGHI_NEW = pd.DataFrame()
    
    BIENBAM_MOTHAU_NEW = pd.DataFrame()
    HSDXTC_NEW = pd.DataFrame()
    KQLCNT_NEW = pd.DataFrame()
    HSDXKT_NEW = pd.DataFrame()
    
    for TBMT, id_tbmt, madinhdanh in zip(GOI_THAU_CT_NEW['MA_TBMT'].values, GOI_THAU_CT_NEW['ID_TBMT'].values, GOI_THAU_CT_NEW['MaDinhDanh'].values):
        link, STT, TITLE = search_TBMT(driver, TBMT)
        driver.get(link)
        wait_load(driver, xpath='//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div/h5', key=TITLE, refresh=True)
        
        # Processing Child section
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
                    LAM_RO_NEW = pd.concat([LAM_RO_NEW, LAM_RO_temp], ignore_index=True)
            elif child_section.text == 'Kiến nghị':
                click_wait(driver, xpath=xpath_child_click)
                check_value = driver.find_element(By.XPATH, '//*[@id="kien-nghi"]/div/div/div').text
                if 'Không có nội dung kiến nghị' not in check_value:
                    KIEN_NGHI_temp = processing_Kien_Nghi(driver, TBMT)
                    KIEN_NGHI_NEW = pd.concat([KIEN_NGHI_NEW, KIEN_NGHI_temp], ignore_index=True)
                    
        # Processing Father section
        xpath_father = '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li'
        Box_info = driver.find_elements(By.XPATH, xpath_father)
        for i in range(len(Box_info)):
            box = driver.find_element(By.XPATH, f'{xpath_father}[{i+1}]')
            xpath_father_click = f'{xpath_father}[{i+1}]/a'
            if box.text == 'Biên bản mở thầu':
                click_wait(driver, xpath=xpath_father_click)
                BIENBAM_MOTHAU_temp = processing_BienBanMoThau(driver, TBMT, id_tbmt)
                BIENBAM_MOTHAU_NEW = pd.concat([BIENBAM_MOTHAU_NEW, BIENBAM_MOTHAU_temp], ignore_index=True)
            elif box.text == 'Biên bản mở E-HSDXTC' or box.text == 'Biên bản mở E-HSĐXTC':
                click_wait(driver, xpath=xpath_father_click)
                HSDXTC_temp = processing_HSDXTC(driver, TBMT, id_tbmt)
                HSDXTC_NEW = pd.concat([HSDXTC_NEW, HSDXTC_temp], ignore_index=True)
            elif box.text == 'Kết quả lựa chọn nhà thầu':
                click_wait(driver, xpath=xpath_father_click)
                KQLCNT_temp = processing_KQChonThau(driver, TBMT, id_tbmt) 
                KQLCNT_NEW = pd.concat([KQLCNT_NEW, KQLCNT_temp], ignore_index=True)

        # Processing another father section
        HSDXKT_temp = processing_HSDXKT(driver, TBMT, id_tbmt, madinhdanh)
        HSDXKT_NEW = pd.concat([HSDXKT_NEW, HSDXKT_temp], ignore_index=True)
        
    return LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW


def template_HUY_THAU(df):
    
    if df.empty:
        return None
    
    print('template_HUY_THAU')
    try:
        url_short = short_link(df['LINK'])
        temp = f"""
🌟 ĐÃ HUỶ THẦU 🌟

- Đơn vị: {df['TenDonVi']}
- Mã TBMT: {df['MA_TBMT']}
- Tên gói thầu: {df['TEN_GOITHAU']}
- Phân loại: Huỷ thầu
- Ngày huỷ thầu: {df['HUYTHAU_NGAY']}
- Lý do huỷ thầu: {df['HUYTHAU_REASON']}
- QĐ phê duyệt: {df['HUYTHAU_SO_QD']} ({df['HUYTHAU_NGAY_QD']}) 
- Link: {url_short}"""
        return temp    
    except Exception as e:
        ib = df['MA_TBMT'].values
        print(f'Skip template_HUY_THAU {ib} as {str(e)}')
        return None



def template_OPEN_BID_1MTHS(df, df_bienbanmothau):
    def processing_TenNhaThauThamGia(df, df_bienbanmothau):
        mess = ''
        BIENBAM_MOTHAU = df_bienbanmothau[df_bienbanmothau['Ma_TBMT'] == df['MA_TBMT'].iloc[0]]
        if not BIENBAM_MOTHAU.empty:
            for i, val in enumerate(BIENBAM_MOTHAU['contractorName_final'].values):
                mess += f'{i+1}. {val}'
                if i < len(BIENBAM_MOTHAU['contractorName_final'].values) - 1:
                    mess += '\n'
        return mess
    
    if df.empty or df_bienbanmothau.empty:
        return None
    
    print('template_OPEN_BID_1MTHS')
    try:
        url_short = short_link(df['LINK'].iloc[0])
        temp = f"""
🌟ĐÃ HOÀN THÀNH MỞ THẦU🌟

- Đơn vị: {df['TenDonVi'].iloc[0]}
- Mã TBMT: {df['MA_TBMT'].iloc[0]}
- Tên gói thầu: {df['TEN_GOITHAU'].iloc[0]}
- Số lượng nhà thầu tham dự: {df['BBMT_SO_NHATHAU_THAMDU'].iloc[0]}
- Thời điểm hoàn thành mở thầu: {df['THOI_DIEM_HOANTHANH_MOTHAU'].iloc[0]}
- Nhà thầu tham gia:
{processing_TenNhaThauThamGia(df, df_bienbanmothau)}
- Link: {url_short}"""
        return temp
    except Exception as e:
        ib = df['MA_TBMT'].iloc[0]
        print(f'Skip template_OPEN_BID_1MTHS {ib} as {str(e)}')
        return None



def template_OPENED_DXKT(df, df_hsdxkt):
    def processing_ThongTinNhaThau(df, df_hsdxkt):
        mess = ''
        ThongTinNhaThau = df_hsdxkt[df_hsdxkt['MA_TBMT'] == df['MA_TBMT'].iloc[0]]
        if not ThongTinNhaThau.empty:
            for i, val in enumerate(ThongTinNhaThau['TEN_NHATHAU'].values):
                mess += f'{i+1}. {val}'
                if i < len(ThongTinNhaThau['TEN_NHATHAU'].values) - 1:
                    mess += '\n'
        return mess
    
    if df.empty or df_hsdxkt.empty:
        return None
    
    print('template_OPENED_DXKT')
    try:
        locale.setlocale(locale.LC_ALL, '')
        url_short = short_link(df['LINK'].iloc[0])
        temp = f"""
🌟HOÀN THÀNH MỞ HSĐXKT🌟

- Đơn vị: {df['TenDonVi'].iloc[0]}
- Mã TBMT: {df['MA_TBMT'].iloc[0]}
- Tên gói thầu: {df['TEN_GOITHAU'].iloc[0]}
- Giá gói thầu: {locale.format_string("%d", df['GIA_GOITHAU'].iloc[0], grouping=True).replace('.', ',')} {df['CCY_GIA_GOITHAU'].iloc[0]}
- Kết quả:
{processing_ThongTinNhaThau(df, df_hsdxkt)}
- Link: {url_short}"""
        return temp
    except Exception as e:
        ib = df['MA_TBMT'].iloc[0]
        print(f'Skip template_OPENED_DXKT {ib} as {str(e)}')
        return None


def Step_2_Processing_ChuaDongThau(driver, GOI_THAU_UPDATE):
    
    GOI_THAU_NEW_S2 = pd.DataFrame()
    GOI_THAU_CT_NEW_S2 = pd.DataFrame()
    GIA_HAN_NEW_S2 = pd.DataFrame()
    
    # Mess
    DATA_HUY_THAU_MESS = []
    DATA_OPEN_BID_1_MTHS_MESS = []
    DATA_HOAN_THANH_MO_HSDXKT_MESS = []
    
    # Data origal
    GOI_THAU_BID01 = GOI_THAU_UPDATE[GOI_THAU_UPDATE['STATUS_BID'] == '"01'].dropna(subset=['MA_TBMT']).reset_index(drop=True)
    
    LAM_RO_NEW = pd.DataFrame()
    KIEN_NGHI_NEW = pd.DataFrame()
    BIENBAM_MOTHAU_NEW = pd.DataFrame()
    HSDXTC_NEW = pd.DataFrame()
    KQLCNT_NEW = pd.DataFrame()
    HSDXKT_NEW = pd.DataFrame()
    
    GOI_THAU_NEW_S2_temp = pd.DataFrame()
    GOI_THAU_CT_NEW_S2_temp = pd.DataFrame()
    GIA_HAN_NEW_S2_temp = pd.DataFrame()
    
    for index, TBMT in enumerate(GOI_THAU_BID01['MA_TBMT'].values):
        link, STT, TITLE = search_TBMT(driver, TBMT)
                
        # Get template HUY TBMT
        if STT == 'Đã hủy TBMT':
            driver.get(link)
            GOI_THAU_NEW_S2_temp = processing_GOI_THAU_Update_module2(driver, STT, GOI_THAU_BID01, index)
            GOI_THAU_CT_NEW_S2_temp, GIA_HAN_NEW_S2_temp = processing_GOI_THAU_CT(driver, GOI_THAU_NEW_S2_temp, 0)
            LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW = Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW_S2_temp)           
            DATA_HUY_THAU_MESS.append(template_HUY_THAU(GOI_THAU_CT_NEW_S2_temp))
                        
        # Get template Dang Xet Thau
        elif STT == 'Đang xét thầu':
            driver.get(link)
            GOI_THAU_NEW_S2_temp = processing_GOI_THAU_Update_module2(driver, STT, GOI_THAU_BID01, index)
            GOI_THAU_CT_NEW_S2_temp, GIA_HAN_NEW_S2_temp = processing_GOI_THAU_CT(driver, GOI_THAU_NEW_S2_temp, 0)
            LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW = Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW_S2_temp)
            
            if GOI_THAU_CT_NEW_S2_temp['PHUONGTHUC_LCNT'].values == 'Một giai đoạn một túi hồ sơ':
                DATA_OPEN_BID_1_MTHS_MESS.append(template_OPEN_BID_1MTHS(GOI_THAU_CT_NEW_S2_temp, BIENBAM_MOTHAU_NEW))
            
            elif GOI_THAU_CT_NEW_S2_temp['PHUONGTHUC_LCNT'].values == 'Một giai đoạn một túi hồ sơ':
                DATA_HOAN_THANH_MO_HSDXKT_MESS.append(template_OPENED_DXKT(GOI_THAU_CT_NEW_S2_temp, HSDXKT_NEW))
                
        GOI_THAU_NEW_S2 = pd.concat([GOI_THAU_NEW_S2, GOI_THAU_NEW_S2_temp], ignore_index=True)
        GOI_THAU_CT_NEW_S2 = pd.concat([GOI_THAU_CT_NEW_S2, GOI_THAU_CT_NEW_S2_temp], ignore_index=True)
        GIA_HAN_NEW_S2 = pd.concat([GIA_HAN_NEW_S2, GIA_HAN_NEW_S2_temp], ignore_index=True)
        
    return GOI_THAU_NEW_S2, GOI_THAU_CT_NEW_S2, GIA_HAN_NEW_S2, DATA_HUY_THAU_MESS, DATA_OPEN_BID_1_MTHS_MESS, DATA_HOAN_THANH_MO_HSDXKT_MESS, LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW


def template_PUBLISH(df):
    def processing_ThongTinNhaThauTrungThau(df):
        driver = None
        mess = ''
        ngay_dang_tai = sqdpd = ngay_pd = None
        try:
            driver = custom_driver()
            TITLE_TBMT = df['TEN_GOITHAU'].iloc[0]
            url_to_visit = df['LINK'].iloc[0]
            driver.get(url_to_visit)
            time.sleep(5)
            wait_load(driver, xpath='//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div/h5', key=TITLE_TBMT, refresh=True)
            KQChonThau, ngay_dang_tai, sqdpd, ngay_pd = processing_KQChonThau(driver, None, None, NgayDangTai_SQDPD=True)
            if not KQChonThau.empty:
                for i, val in enumerate(KQChonThau['orgFullname'].values):
                    mess += f'{i+1}. {val}'
                    if i < len(KQChonThau['orgFullname'].values) - 1:
                        mess += '\n'
        finally:
            if driver:
                driver.quit()
            return mess, ngay_dang_tai, sqdpd, ngay_pd
    
    if df.empty:
        return None
    
    print('template_PUBLISH')    
    try:
        mess, ngay_dang_tai, sqdpd, ngay_pd = processing_ThongTinNhaThauTrungThau(df)
        locale.setlocale(locale.LC_ALL, '')
        url_short = short_link(df['LINK'].iloc[0])
        temp = f"""
🌟CÓ NHÀ THẦU TRÚNG THẦU🌟

- Đơn vị: {df['TenDonVi'].iloc[0]}
- Mã TBMT: {df['MA_TBMT'].iloc[0]}
- Tên gói thầu: {df['TEN_GOITHAU'].iloc[0]}
- Giá gói thầu: {locale.format_string("%d", df['GIA_GOITHAU'].iloc[0], grouping=True).replace('.', ',')} {df['CCY_GIA_GOITHAU'].iloc[0]}
- Giá trúng thầu: {locale.format_string("%d", df['bidWiningPrice'].iloc[0], grouping=True).replace('.', ',')} {df['CCY_GIA_GOITHAU'].iloc[0]}
- Ngày đăng tải KQLCNT: {ngay_dang_tai}
- QĐ phê duyệt KQLCNT: {sqdpd} ({ngay_pd})
- Kết quả:
{mess}
- Link: {url_short}"""
        return temp
    except Exception as e:
        ib = df['MA_TBMT'].iloc[0]
        print(f'Skip template_PUBLISH {ib} as {str(e)}')
        return None



def Step_3_Processing_DangXetThau_v1(driver, GOI_THAU_UPDATE):
    
    GOI_THAU_NEW_S3 = pd.DataFrame()
    GOI_THAU_CT_NEW_S3 = pd.DataFrame()
    GIA_HAN_NEW_S3 = pd.DataFrame()
    
    # Mess
    DATA_HUY_THAU_MESS = []
    DATA_OPENED_BID_PUBLISH_MESS = []
    
    # Data origal
    GOI_THAU_BID_OPENED_V1 = GOI_THAU_UPDATE[(GOI_THAU_UPDATE['STATUS_BID'] == 'OPENED_BID') | (GOI_THAU_UPDATE['STATUS_BID'] == 'OPENED_DXTC')].dropna(subset=['MA_TBMT'])
    
    
    LAM_RO_NEW = pd.DataFrame()
    KIEN_NGHI_NEW = pd.DataFrame()
    BIENBAM_MOTHAU_NEW = pd.DataFrame()
    HSDXTC_NEW = pd.DataFrame()
    KQLCNT_NEW = pd.DataFrame()
    HSDXKT_NEW = pd.DataFrame()
    
    GOI_THAU_NEW_S3_temp = pd.DataFrame()
    GOI_THAU_CT_NEW_S3_temp = pd.DataFrame()
    GIA_HAN_NEW_S3_temp = pd.DataFrame()
    
    for index, TBMT in enumerate(GOI_THAU_BID_OPENED_V1['MA_TBMT'].values):
        link, STT, TITLE = search_TBMT(driver, TBMT)
        
        # Get template HUY TBMT
        if STT == 'Đã hủy TBMT':
            driver.get(link)
            GOI_THAU_NEW_S3_temp = processing_GOI_THAU_Update_module2(driver, STT, GOI_THAU_BID_OPENED_V1, index)
            GOI_THAU_CT_NEW_S3_temp, GIA_HAN_NEW_S3_temp = processing_GOI_THAU_CT(driver, GOI_THAU_NEW_S3_temp, 0)            
            DATA_HUY_THAU_MESS.append(template_HUY_THAU(GOI_THAU_CT_NEW_S3_temp))
            LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW = Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW_S3_temp)

        # Get template
        elif STT == 'Có nhà thầu trúng thầu':
            driver.get(link)
            GOI_THAU_NEW_S3_temp = processing_GOI_THAU_Update_module2(driver, STT, GOI_THAU_BID_OPENED_V1, index)
            GOI_THAU_CT_NEW_S3_temp, GIA_HAN_NEW_S3_temp = processing_GOI_THAU_CT(driver, GOI_THAU_NEW_S3_temp, 0)
            DATA_OPENED_BID_PUBLISH_MESS.append(template_PUBLISH(GOI_THAU_CT_NEW_S3_temp))
            LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW = Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW_S3_temp)    
        
        GOI_THAU_NEW_S3 = pd.concat([GOI_THAU_NEW_S3, GOI_THAU_NEW_S3_temp], ignore_index=True)    
        GOI_THAU_CT_NEW_S3 = pd.concat([GOI_THAU_CT_NEW_S3, GOI_THAU_CT_NEW_S3_temp], ignore_index=True)
        GIA_HAN_NEW_S3 = pd.concat([GIA_HAN_NEW_S3, GIA_HAN_NEW_S3_temp], ignore_index=True)
    
    return GOI_THAU_NEW_S3, GOI_THAU_CT_NEW_S3, GIA_HAN_NEW_S3, DATA_HUY_THAU_MESS, DATA_OPENED_BID_PUBLISH_MESS, LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW


def template_APPROVED_DXKT(df, df_hsdxkt):
    
    def processing_ThongTinDanhGia(df, df_hsdxkt):
        HSDXKT_DF = df_hsdxkt[df_hsdxkt['MA_TBMT'] == df['MA_TBMT'].iloc[0]]
        if not HSDXKT_DF.empty:
            for i, val in enumerate(HSDXKT_DF['KETQUA_DANHGIA'].values):
                mess += f'{i+1}. {val}'
                if i < len(HSDXKT_DF['KETQUA_DANHGIA'].values) - 1:
                    mess += '\n'
        return mess
        
    if df.empty or df_hsdxkt.empty:
        return None
    
    print('template_APPROVED_DXKT')
    try:
        mess = processing_ThongTinDanhGia(df)
        locale.setlocale(locale.LC_ALL, '')
        url_short = short_link(df['LINK'].iloc[0])
        temp = f"""
🌟HOÀN THÀNH ĐÁNH GIÁ HSĐXKT🌟

- Đơn vị: {df['TenDonVi'].iloc[0]}
- Mã TBMT: {df['MA_TBMT'].iloc[0]}
- Tên gói thầu: {df['TEN_GOITHAU'].iloc[0]}
- Giá gói thầu: {locale.format_string("%d", df['GIA_GOITHAU'].iloc[0], grouping=True).replace('.', ',')} {df['CCY_GIA_GOITHAU'].iloc[0]}
- Kết quả:
{mess}
- Link: {url_short}"""
        return temp
    except Exception as e:
        ib = df['MA_TBMT'].iloc[0]
        print(f'Skip template_APPROVED_DXKT {ib} as {str(e)}')
        return None


def Step_3_Processing_DangXetThau_v2(driver, GOI_THAU_UPDATE):
    
    GOI_THAU_NEW_S3_2 = pd.DataFrame()
    GOI_THAU_CT_NEW_S3_2 = pd.DataFrame()
    GIA_HAN_NEW_S3_2 = pd.DataFrame()
    
    # Mess
    DATA_HUY_THAU_MESS = []
    DATA_APPROVED_DXKT_MESS = []
    
    # Data origal
    GOI_THAU_BID_OPENED_V2 = GOI_THAU_UPDATE[GOI_THAU_UPDATE['STATUS_BID'] == 'OPEN_DXKT'].dropna(subset=['MA_TBMT']).reset_index(drop=True)
    
    LAM_RO_NEW = pd.DataFrame()
    KIEN_NGHI_NEW = pd.DataFrame()
    BIENBAM_MOTHAU_NEW = pd.DataFrame()
    HSDXTC_NEW = pd.DataFrame()
    KQLCNT_NEW = pd.DataFrame()
    HSDXKT_NEW = pd.DataFrame()
    
    GOI_THAU_NEW_S3_2_temp = pd.DataFrame()
    GOI_THAU_CT_NEW_2_S3_temp = pd.DataFrame()
    GIA_HAN_NEW_S3_2_temp = pd.DataFrame()
    
    for index, TBMT in enumerate(GOI_THAU_BID_OPENED_V2['MA_TBMT'].values):
        link, STT, TITLE = search_TBMT(driver, TBMT)
        
        # Get template HUY TBMT
        if STT == 'Đã hủy TBMT':
            driver.get(link)
            GOI_THAU_NEW_S3_2_temp = processing_GOI_THAU_Update_module2(driver, STT, GOI_THAU_BID_OPENED_V2, index)
            GOI_THAU_CT_NEW_S3_2_temp, GIA_HAN_NEW_S3_2_temp = processing_GOI_THAU_CT(driver, GOI_THAU_NEW_S3_2_temp, 0)            
            DATA_HUY_THAU_MESS.append(template_HUY_THAU(GOI_THAU_CT_NEW_S3_2_temp))
            LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW = Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW_S3_2_temp)    

        # Get template
        else:
            driver.get(link)
            GOI_THAU_NEW_S3_2_temp = processing_GOI_THAU_Update_module2(driver, STT, GOI_THAU_BID_OPENED_V2, index)
            GOI_THAU_CT_NEW_2_S3_temp, GIA_HAN_NEW_S3_2_temp = processing_GOI_THAU_CT(driver, GOI_THAU_NEW_S3_2_temp, 0)
            LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW = Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW_S3_2_temp)   
            DATA_APPROVED_DXKT_MESS.append(template_APPROVED_DXKT(GOI_THAU_CT_NEW_S3_2_temp, HSDXKT_NEW))
        
        GOI_THAU_NEW_S3_2 = pd.concat([GOI_THAU_NEW_S3_2, GOI_THAU_NEW_S3_2_temp], ignore_index=True)     
        GOI_THAU_CT_NEW_S3_2 = pd.concat([GOI_THAU_CT_NEW_S3_2, GOI_THAU_CT_NEW_2_S3_temp], ignore_index=True)
        GIA_HAN_NEW_S3_2 = pd.concat([GIA_HAN_NEW_S3_2, GIA_HAN_NEW_S3_2_temp], ignore_index=True)
    
    return GOI_THAU_NEW_S3_2, GOI_THAU_CT_NEW_S3_2, GIA_HAN_NEW_S3_2, DATA_HUY_THAU_MESS, DATA_APPROVED_DXKT_MESS, LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW


def template_OPEND_DXTC(df, df_hsdxtc):
    def processing_ThongTinDanhGia(df, df_hsdxtc):
        mess = ''
        HSDXTC_DF = df_hsdxtc[df_hsdxtc['MA_TBMT'] == df['MA_TBMT'].iloc[0]]
        if not HSDXTC_DF.empty:
            for i, val in enumerate(HSDXTC_DF['KETQUA_DANHGIA'].values):
                mess += f'{i+1}. {val}'
                if i < len(HSDXTC_DF['KETQUA_DANHGIA'].values) - 1:
                    mess += '\n'
        return mess
        
    if df.empty or df_hsdxtc.empty:
        return None
    
    print('template_OPEND_DXTC')
    try:
        mess = processing_ThongTinDanhGia(df, df_hsdxtc)
        locale.setlocale(locale.LC_ALL, '')
        url_short = short_link(df['LINK'].iloc[0])
        temp = f"""
🌟HOÀN THÀNH MỞ HSĐXTC🌟

- Đơn vị: {df['TenDonVi'].iloc[0]}
- Mã TBMT: {df['MA_TBMT'].iloc[0]}
- Tên gói thầu: {df['TEN_GOITHAU'].iloc[0]}
- Giá gói thầu: {locale.format_string("%d", df['GIA_GOITHAU'].iloc[0], grouping=True).replace('.', ',')} {df['CCY_GIA_GOITHAU'].iloc[0]}
- Kết quả:
{mess}
- Link: {url_short}"""
        return temp
    except Exception as e:
        ib = df['MA_TBMT'].iloc[0]
        print(f'Skip template_OPEND_DXTC {ib} as {str(e)}')
        return None


def Step_3_Processing_DangXetThau_v3(driver, GOI_THAU_UPDATE):
    
    GOI_THAU_NEW_S3_3 = pd.DataFrame()
    GOI_THAU_CT_NEW_S3_3 = pd.DataFrame()
    GIA_HAN_NEW_S3_3 = pd.DataFrame()
    
    # Mess
    DATA_HUY_THAU_MESS = []
    DATA_OPENED_DXTC_MESS = []
    
    # Data origal
    GOI_THAU_BID_OPENED_V3 = GOI_THAU_UPDATE[GOI_THAU_UPDATE['STATUS_BID'] == 'APPROVED_DXKT'].dropna(subset=['MA_TBMT'])
    
    LAM_RO_NEW = pd.DataFrame()
    KIEN_NGHI_NEW = pd.DataFrame()
    BIENBAM_MOTHAU_NEW = pd.DataFrame()
    HSDXTC_NEW = pd.DataFrame()
    KQLCNT_NEW = pd.DataFrame()
    HSDXKT_NEW = pd.DataFrame()
    
    
    GOI_THAU_NEW_S3_3_temp = pd.DataFrame()
    GOI_THAU_CT_NEW_S3_3_temp = pd.DataFrame()
    GIA_HAN_NEW_S3_3_temp = pd.DataFrame()
    
    
    for index, TBMT in enumerate(GOI_THAU_BID_OPENED_V3['MA_TBMT'].values):
        link, STT, TITLE = search_TBMT(driver, TBMT)
        
        # Get template HUY TBMT
        if STT == 'Đã hủy TBMT':
            driver.get(link)
            GOI_THAU_NEW_S3_3_temp = processing_GOI_THAU_Update_module2(driver, STT, GOI_THAU_BID_OPENED_V3, index)
            GOI_THAU_CT_NEW_S3_3_temp, GIA_HAN_NEW_S3_3_temp = processing_GOI_THAU_CT(driver, GOI_THAU_NEW_S3_3_temp, 0)            
            LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW = Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW_S3_3_temp)
            DATA_HUY_THAU_MESS.append(template_HUY_THAU(GOI_THAU_CT_NEW_S3_3_temp))
            
        # Get template
        else:
            driver.get(link)
            GOI_THAU_NEW_S3_3_temp = processing_GOI_THAU_Update_module2(driver, STT, GOI_THAU_BID_OPENED_V3, index)
            GOI_THAU_CT_NEW_S3_3_temp, GIA_HAN_NEW_S3_3_temp = processing_GOI_THAU_CT(driver, GOI_THAU_NEW_S3_3_temp, 0) 
            LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW = Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW_S3_3_temp)   
            DATA_OPENED_DXTC_MESS.append(template_OPEND_DXTC(GOI_THAU_CT_NEW_S3_3_temp, HSDXTC_NEW))
        
        GOI_THAU_NEW_S3_3 = pd.concat([GOI_THAU_NEW_S3_3, GOI_THAU_NEW_S3_3_temp], ignore_index=True)
        GOI_THAU_CT_NEW_S3_3 = pd.concat([GOI_THAU_CT_NEW_S3_3, GOI_THAU_CT_NEW_S3_3_temp], ignore_index=True)
        GIA_HAN_NEW_S3_3 = pd.concat([GIA_HAN_NEW_S3_3, GIA_HAN_NEW_S3_3_temp], ignore_index=True)
    
    return GOI_THAU_NEW_S3_3, GOI_THAU_CT_NEW_S3_3, GIA_HAN_NEW_S3_3, DATA_HUY_THAU_MESS, DATA_OPENED_DXTC_MESS, LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW


def template_TBMT(df):
    
    if df.empty:
        return None
    
    print('template_TBMT')
    try:
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
    except Exception as e:
        ib = df['MA_TBMT'].values
        print(f'Skip template_TBMT {ib} as {str(e)}')
        return None


def template_GIA_HAN(df_giahan, GOI_THAU_CT_UPDATE):
    
    if df_giahan.empty or GOI_THAU_CT_UPDATE.empty:
        return None
    
    print('template_GIA_HAN')
    try:
        df = GOI_THAU_CT_UPDATE[GOI_THAU_CT_UPDATE['MA_TBMT'] == df_giahan['MA_TBMT'].iloc[0]]    
        url_short = short_link(df['LINK'].iloc[0])
        temp = f"""
🌟 GIA HẠN GÓI THẦU 🌟

- Đơn vị: {df['TenDonVi'].iloc[0]}
- Mã TBMT: {df['MA_TBMT'].iloc[0]}
- Tên gói thầu: {df['TEN_GOITHAU'].iloc[0]}
- Lần gia hạn: {df_giahan['LAN_GIAHAN']}
- Lý do: {df_giahan['LYDO']}
- Ngày gia hạn: {df_giahan['NGAY_GIAHAN']}
- Thời điểm mở thầu cũ: {df_giahan['THOIDIEM_MOTHAU_CU']}
- Thời điểm đóng thầu cũ: {df_giahan['THOIDIEM_DONGTHAU_CU']}
- Thời điểm mở thầu mới: {df_giahan['THOIDIEM_MOTHAU_MOI']}
- Thời điểm đóng thầu mới: {df_giahan['THOIDIEM_DONGTHAU_MOI']}
- Link: {url_short}"""
        return temp
    except Exception as e:
        ib = df['MA_TBMT'].iloc[0]
        print(f'Skip template_GIA_HAN {ib} as {str(e)}')
        return None


def template_LAM_RO(df_lamro, GOI_THAU_CT_UPDATE):
    print('template_LAM_RO')
    
    if df_lamro.empty or GOI_THAU_CT_UPDATE.empty:
        return None
    try:
        df = GOI_THAU_CT_UPDATE[GOI_THAU_CT_UPDATE['MA_TBMT'] == df_lamro['Ma_TBMT'].iloc[0]]
        url_short = short_link(df['LINK'].iloc[0])
        temp = f"""
🌟 LÀM RÕ 🌟

- Đơn vị: {df['TenDonVi'].iloc[0]}
- Mã TBMT: {df['MA_TBMT'].iloc[0]}
- Tên gói thầu: {df['TEN_GOITHAU'].iloc[0]}
- Ngày yêu cầu làm rõ: {df_lamro['YEUCAU_LAMRO_NGAY']}
- Tên yêu cầu làm rõ: {df_lamro['YEUCAU_LAMRO_TEN']}
- Link: {url_short}"""
        return temp
    except Exception as e:
        ib = df['MA_TBMT'].iloc[0]
        print(f'Skip template_LAM_RO {ib} as {str(e)}')
        return None


def template_KIEN_NGHI(df_kiennghi, GOI_THAU_CT_UPDATE):
    print('template_KIEN_NGHI')
    
    if df_kiennghi.empty or GOI_THAU_CT_UPDATE.empty:
        return None
    
    try:
        df = GOI_THAU_CT_UPDATE[GOI_THAU_CT_UPDATE['MA_TBMT'] == df_kiennghi['MA_TBMT'].iloc[0]]
        url_short = short_link(df['LINK'].iloc[0])
        temp = f"""
🌟 KIẾN NGHỊ 🌟

- Đơn vị: {df['TenDonVi'].iloc[0]}
- Mã TBMT: {df['MA_TBMT'].iloc[0]}
- Tên gói thầu: {df['TEN_GOITHAU'].iloc[0]}
- Ngày kiến nghị: {None}
- Tên kiến nghị: {df_kiennghi['TEN_KIENNGHI']}
- Đơn vị kiến nghị: {None}
- Link: {url_short}"""
        return temp
    except Exception as e:
        ib = df['MA_TBMT'].iloc[0]
        print(f'Skip template_KIEN_NGHI {ib} as {str(e)}')
        return None


def module_2(driver, all_df):
    
    KHLCNT = all_df['2.1.KHLCNT']
    GOI_THAU = all_df['2.1.GOI_THAU']
    GOI_THAU_CT = all_df['2.1.GOI_THAU_CT']
    GIA_HAN = all_df['2.1.GIA_HAN']
    LAM_RO = all_df['2.1.LAM_RO']
    KIEN_NGHI = all_df['2.1.KIEN_NGHI']
    BIENBAM_MOTHAU = all_df['2.1.BIENBAN_MOTHAU']
    HSDXTC = all_df['2.1.HSDXTC']
    KQLCNT = all_df['2.1.KQLCNT']
    HSDXKT = all_df['2.1.HSDXKT']
    
    # Create temp step 1
    TBMT_MOI_MESS_ALL = []
    GIA_HAN_MESS_ALL = []
    LAM_RO_MESS_ALL = []
    KIEN_NGHI_MESS_ALL = []
    
    # All mess from update step 2 to final
    HUY_THAU_MESS_ALL = []
    OPENED_BID_1_MTHS_MESS_ALL = []
    HOAN_THANH_MO_HSDXKT_MESS_ALL = []
    OPEN_BID_PUBLISH_MESS_ALL = []
    APPROVED_DXKT_MESS_ALL = []    
    OPENED_DXTC_MESS_ALL = []
    
    # Search from TBMT data base using for UPDATE
    GOI_THAU_NEW_UPDATE_ALL = pd.DataFrame()
    GOI_THAU_CT_NEW_UPDATE_ALL = pd.DataFrame()
    GIA_HAN_NEW_UPDATE_ALL = pd.DataFrame()
    LAM_RO_NEW_UPDATE_ALL = pd.DataFrame()
    KIEN_NGHI_NEW_UPDATE_ALL = pd.DataFrame()
    BIENBAM_MOTHAU_NEW_UPDATE_ALL = pd.DataFrame()
    HSDXTC_NEW_UPDATE_ALL = pd.DataFrame()
    KQLCNT_NEW_UPDATE_ALL = pd.DataFrame()
    HSDXKT_NEW_UPDATE_ALL = pd.DataFrame()
    
    
    
    # Step 1 Search TBMT Null
    """
    Search for new data from old data where TBMT is null.
    New data found do not need to be searched again or updated.
    Please concatenate after updating all old data.
    """
    print('Step 1 module 2')
    # All new data in here will concat to data base after done all steps
    GOI_THAU_NEW, GOI_THAU_CT_NEW, GIA_HAN_NEW = Step_1_Update_TBMT(driver, GOI_THAU)
    if not GOI_THAU_CT_NEW.empty:
        LAM_RO_NEW, KIEN_NGHI_NEW, BIENBAM_MOTHAU_NEW, HSDXTC_NEW, KQLCNT_NEW, HSDXKT_NEW = Step_1_2_Update_All_Child(driver, GOI_THAU_CT_NEW)
        
        # All mess from search TBMT null step 1
        TBMT_MOI_MESS_ALL = [template_TBMT(GOI_THAU_CT_NEW.iloc[i]) for i in range(len(GOI_THAU_CT_NEW))]
        GIA_HAN_MESS_ALL = [template_GIA_HAN(GIA_HAN_NEW.iloc[i], GOI_THAU_CT_NEW) for i in range(len(GIA_HAN_NEW))]
        LAM_RO_MESS_ALL = [template_LAM_RO(LAM_RO_NEW.iloc[i], GOI_THAU_CT_NEW) for i in range(len(LAM_RO_NEW))]
        KIEN_NGHI_MESS_ALL = [template_LAM_RO(KIEN_NGHI_NEW.iloc[i], GOI_THAU_CT_NEW) for i in range(len(KIEN_NGHI_NEW))]
    
    
    # Step 2
    """
    In Step 2 through the final step, use old data to search and update.
    Please update after completion for all; updating during Step 2 could cause conflicts with subsequent steps.
    """
    print('Step 2 module 2')
    GOI_THAU_NEW_S2, GOI_THAU_CT_NEW_S2, GIA_HAN_NEW_S2, DATA_HUY_THAU_MESS, DATA_OPENED_BID_1_MTHS_MESS, DATA_HOAN_THANH_MO_HSDXKT_MESS, LAM_RO_NEW_S2, KIEN_NGHI_NEW_S2, BIENBAM_MOTHAU_NEW_S2, HSDXTC_NEW_S2, KQLCNT_NEW_S2, HSDXKT_NEW_S2 = Step_2_Processing_ChuaDongThau(driver, GOI_THAU_CT)
    
    # Append MESS
    HUY_THAU_MESS_ALL.extend(DATA_HUY_THAU_MESS)
    OPENED_BID_1_MTHS_MESS_ALL.extend(DATA_OPENED_BID_1_MTHS_MESS)
    HOAN_THANH_MO_HSDXKT_MESS_ALL.extend(DATA_HOAN_THANH_MO_HSDXKT_MESS)
    
    # Append all update data
    GOI_THAU_NEW_UPDATE_ALL = pd.concat([GOI_THAU_NEW_UPDATE_ALL, GOI_THAU_NEW_S2], ignore_index=True)
    GOI_THAU_CT_NEW_UPDATE_ALL = pd.concat([GOI_THAU_CT_NEW_UPDATE_ALL, GOI_THAU_CT_NEW_S2], ignore_index=True)
    GIA_HAN_NEW_UPDATE_ALL = pd.concat([GIA_HAN_NEW_UPDATE_ALL, GIA_HAN_NEW_S2], ignore_index=True)
    LAM_RO_NEW_UPDATE_ALL = pd.concat([LAM_RO_NEW_UPDATE_ALL, LAM_RO_NEW_S2], ignore_index=True)
    KIEN_NGHI_NEW_UPDATE_ALL = pd.concat([KIEN_NGHI_NEW_UPDATE_ALL, KIEN_NGHI_NEW_S2], ignore_index=True)
    BIENBAM_MOTHAU_NEW_UPDATE_ALL = pd.concat([BIENBAM_MOTHAU_NEW_UPDATE_ALL, BIENBAM_MOTHAU_NEW_S2], ignore_index=True)
    HSDXTC_NEW_UPDATE_ALL = pd.concat([HSDXTC_NEW_UPDATE_ALL, HSDXTC_NEW_S2], ignore_index=True)
    KQLCNT_NEW_UPDATE_ALL = pd.concat([KQLCNT_NEW_UPDATE_ALL, KQLCNT_NEW_S2], ignore_index=True)
    HSDXKT_NEW_UPDATE_ALL = pd.concat([HSDXKT_NEW_UPDATE_ALL, HSDXKT_NEW_S2], ignore_index=True)
    
    
    # Step 3
    print('Step 3 module 2')
    GOI_THAU_NEW_S3, GOI_THAU_CT_NEW_S3, GIA_HAN_NEW_S3, DATA_HUY_THAU_MESS, DATA_OPEN_BID_PUBLISH_MESS, LAM_RO_NEW_S3, KIEN_NGHI_NEW_S3, BIENBAM_MOTHAU_NEW_S3, HSDXTC_NEW_S3, KQLCNT_NEW_S3, HSDXKT_NEW_S3 = Step_3_Processing_DangXetThau_v1(driver, GOI_THAU_UPDATE=GOI_THAU)
    
    # Append MESS
    HUY_THAU_MESS_ALL.extend(DATA_HUY_THAU_MESS)
    OPEN_BID_PUBLISH_MESS_ALL.extend(DATA_OPEN_BID_PUBLISH_MESS)
    
    # Append all update data
    GOI_THAU_NEW_UPDATE_ALL = pd.concat([GOI_THAU_NEW_UPDATE_ALL, GOI_THAU_NEW_S3], ignore_index=True)
    GOI_THAU_CT_NEW_UPDATE_ALL = pd.concat([GOI_THAU_CT_NEW_UPDATE_ALL, GOI_THAU_CT_NEW_S3], ignore_index=True)
    GIA_HAN_NEW_UPDATE_ALL = pd.concat([GIA_HAN_NEW_UPDATE_ALL, GIA_HAN_NEW_S3], ignore_index=True)
    LAM_RO_NEW_UPDATE_ALL = pd.concat([LAM_RO_NEW_UPDATE_ALL, LAM_RO_NEW_S3], ignore_index=True)
    KIEN_NGHI_NEW_UPDATE_ALL = pd.concat([KIEN_NGHI_NEW_UPDATE_ALL, KIEN_NGHI_NEW_S3], ignore_index=True)
    BIENBAM_MOTHAU_NEW_UPDATE_ALL = pd.concat([BIENBAM_MOTHAU_NEW_UPDATE_ALL, BIENBAM_MOTHAU_NEW_S3], ignore_index=True)
    HSDXTC_NEW_UPDATE_ALL = pd.concat([HSDXTC_NEW_UPDATE_ALL, HSDXTC_NEW_S3], ignore_index=True)
    KQLCNT_NEW_UPDATE_ALL = pd.concat([KQLCNT_NEW_UPDATE_ALL, KQLCNT_NEW_S3], ignore_index=True)
    HSDXKT_NEW_UPDATE_ALL = pd.concat([HSDXKT_NEW_UPDATE_ALL, HSDXKT_NEW_S3], ignore_index=True)
    
    
    # Step 4
    print('Step 4 module 2')
    GOI_THAU_NEW_S3_2, GOI_THAU_CT_NEW_S3_2, GIA_HAN_NEW_S3_2, DATA_HUY_THAU_MESS, DATA_APPROVED_DXKT_MESS, LAM_RO_NEW_S3_2, KIEN_NGHI_NEW_S3_2, BIENBAM_MOTHAU_NEW_S3_2, HSDXTC_NEW_S3_2, KQLCNT_NEW_S3_2, HSDXKT_NEW_S3_2 = Step_3_Processing_DangXetThau_v2(driver, GOI_THAU_UPDATE=GOI_THAU)
    
    # Append MESS
    HUY_THAU_MESS_ALL.extend(DATA_HUY_THAU_MESS)
    APPROVED_DXKT_MESS_ALL.extend(DATA_APPROVED_DXKT_MESS)
    
    # Append all update data
    GOI_THAU_NEW_UPDATE_ALL = pd.concat([GOI_THAU_NEW_UPDATE_ALL, GOI_THAU_NEW_S3_2], ignore_index=True)
    GOI_THAU_CT_NEW_UPDATE_ALL = pd.concat([GOI_THAU_CT_NEW_UPDATE_ALL, GOI_THAU_CT_NEW_S3_2], ignore_index=True)
    GIA_HAN_NEW_UPDATE_ALL = pd.concat([GIA_HAN_NEW_UPDATE_ALL, GIA_HAN_NEW_S3_2], ignore_index=True)
    LAM_RO_NEW_UPDATE_ALL = pd.concat([LAM_RO_NEW_UPDATE_ALL, LAM_RO_NEW_S3_2], ignore_index=True)
    KIEN_NGHI_NEW_UPDATE_ALL = pd.concat([KIEN_NGHI_NEW_UPDATE_ALL, KIEN_NGHI_NEW_S3_2], ignore_index=True)
    BIENBAM_MOTHAU_NEW_UPDATE_ALL = pd.concat([BIENBAM_MOTHAU_NEW_UPDATE_ALL, BIENBAM_MOTHAU_NEW_S3_2], ignore_index=True)
    HSDXTC_NEW_UPDATE_ALL = pd.concat([HSDXTC_NEW_UPDATE_ALL, HSDXTC_NEW_S3_2], ignore_index=True)
    KQLCNT_NEW_UPDATE_ALL = pd.concat([KQLCNT_NEW_UPDATE_ALL, KQLCNT_NEW_S3_2], ignore_index=True)
    HSDXKT_NEW_UPDATE_ALL = pd.concat([HSDXKT_NEW_UPDATE_ALL, HSDXKT_NEW_S3_2], ignore_index=True)
    
    # Step 5
    print('Step 5 module 2')
    GOI_THAU_NEW_S3_3, GOI_THAU_CT_NEW_S3_3, GIA_HAN_NEW_S3_3, DATA_HUY_THAU_MESS, DATA_OPENED_DXTC_MESS, LAM_RO_NEW_S3_3, KIEN_NGHI_NEW_S3_3, BIENBAM_MOTHAU_NEW_S3_3, HSDXTC_NEW_S3_3, KQLCNT_NEW_S3_3, HSDXKT_NEW_S3_3 = Step_3_Processing_DangXetThau_v3(driver, GOI_THAU_UPDATE=GOI_THAU)
    
    # Append MESS
    HUY_THAU_MESS_ALL.extend(DATA_HUY_THAU_MESS)
    OPENED_DXTC_MESS_ALL.extend(DATA_OPENED_DXTC_MESS)
    
    # Append all update data
    GOI_THAU_NEW_UPDATE_ALL = pd.concat([GOI_THAU_NEW_UPDATE_ALL, GOI_THAU_NEW_S3_3], ignore_index=True)
    GOI_THAU_CT_NEW_UPDATE_ALL = pd.concat([GOI_THAU_CT_NEW_UPDATE_ALL, GOI_THAU_CT_NEW_S3_3], ignore_index=True)
    GIA_HAN_NEW_UPDATE_ALL = pd.concat([GIA_HAN_NEW_UPDATE_ALL, GIA_HAN_NEW_S3_3], ignore_index=True)
    LAM_RO_NEW_UPDATE_ALL = pd.concat([LAM_RO_NEW_UPDATE_ALL, LAM_RO_NEW_S3_3], ignore_index=True)
    KIEN_NGHI_NEW_UPDATE_ALL = pd.concat([KIEN_NGHI_NEW_UPDATE_ALL, KIEN_NGHI_NEW_S3_3], ignore_index=True)
    BIENBAM_MOTHAU_NEW_UPDATE_ALL = pd.concat([BIENBAM_MOTHAU_NEW_UPDATE_ALL, BIENBAM_MOTHAU_NEW_S3_3], ignore_index=True)
    HSDXTC_NEW_UPDATE_ALL = pd.concat([HSDXTC_NEW_UPDATE_ALL, HSDXTC_NEW_S3_3], ignore_index=True)
    KQLCNT_NEW_UPDATE_ALL = pd.concat([KQLCNT_NEW_UPDATE_ALL, KQLCNT_NEW_S3_3], ignore_index=True)
    HSDXKT_NEW_UPDATE_ALL = pd.concat([HSDXKT_NEW_UPDATE_ALL, HSDXKT_NEW_S3_3], ignore_index=True)


    """Only GOI_THAU need update first IN STEP 1"""
    if not GOI_THAU_CT_NEW.empty:
        GOI_THAU = Update_DataFrame(df_old=GOI_THAU, df_new=GOI_THAU_NEW, header_target='TEN_GOITHAU') 
                
        # Concat all data step 1 
        GOI_THAU_CT = pd.concat([GOI_THAU_CT, GOI_THAU_CT_NEW], ignore_index=True)
        GIA_HAN = pd.concat([GIA_HAN, GIA_HAN_NEW], ignore_index=True)
        LAM_RO = pd.concat([LAM_RO, LAM_RO_NEW], ignore_index=True)
        KIEN_NGHI = pd.concat([KIEN_NGHI, KIEN_NGHI_NEW], ignore_index=True)
        BIENBAM_MOTHAU = pd.concat([BIENBAM_MOTHAU, BIENBAM_MOTHAU_NEW], ignore_index=True)
        HSDXTC = pd.concat([HSDXTC, HSDXTC_NEW], ignore_index=True)
        KQLCNT = pd.concat([KQLCNT, KQLCNT_NEW], ignore_index=True)
        HSDXKT = pd.concat([HSDXKT, HSDXKT_NEW], ignore_index=True)
    
    
    # UPDATE DATA
    GOI_THAU = Update_DataFrame(df_old=GOI_THAU, df_new=GOI_THAU_NEW_UPDATE_ALL, header_target='TEN_GOITHAU')
    GOI_THAU_CT = Update_DataFrame(df_old=GOI_THAU_CT, df_new=GOI_THAU_CT_NEW_UPDATE_ALL, header_target='TEN_GOITHAU')
    GIA_HAN = Update_DataFrame(df_old=GIA_HAN, df_new=GIA_HAN_NEW_UPDATE_ALL, header_target='MA_TBMT')
    LAM_RO = Update_DataFrame(df_old=LAM_RO, df_new=LAM_RO_NEW_UPDATE_ALL, header_target='Ma_TBMT')
    KIEN_NGHI = Update_DataFrame(df_old=KIEN_NGHI, df_new=KIEN_NGHI_NEW_UPDATE_ALL, header_target='MA_TBMT')
    BIENBAM_MOTHAU = Update_DataFrame(df_old=BIENBAM_MOTHAU, df_new=BIENBAM_MOTHAU_NEW_UPDATE_ALL, header_target='Ma_TBMT')
    HSDXTC = Update_DataFrame(df_old=HSDXTC, df_new=HSDXTC_NEW_UPDATE_ALL, header_target='Ma_TBMT')
    KQLCNT = Update_DataFrame(df_old=KQLCNT, df_new=KQLCNT_NEW_UPDATE_ALL, header_target='Ma_TBMT')
    HSDXKT = Update_DataFrame(df_old=HSDXKT, df_new=HSDXKT_NEW_UPDATE_ALL, header_target='MA_TBMT')
    
    
    dict_data = {
        '2.1.KHLCNT': KHLCNT,
        '2.1.GOI_THAU': GOI_THAU,
        '2.1.GOI_THAU_CT': GOI_THAU_CT,
        '2.1.GIA_HAN': GIA_HAN,
        '2.1.LAM_RO': LAM_RO,
        '2.1.KIEN_NGHI': KIEN_NGHI,
        '2.1.BIENBAN_MOTHAU': BIENBAM_MOTHAU,
        '2.1.HSDXKT': HSDXKT,
        '2.1.HSDXTC': HSDXTC,
        '2.1.KQLCNT': KQLCNT
    }
    
    # Clear dup data
    list_of_sheets = ['2.1.KHLCNT', '2.1.GOI_THAU', '2.1.GOI_THAU_CT', '2.1.GIA_HAN', '2.1.LAM_RO',
                  '2.1.KIEN_NGHI', '2.1.BIENBAN_MOTHAU', '2.1.HSDXKT', '2.1.HSDXTC', '2.1.KQLCNT']
    list_of_headers = ['planName', 'TEN_GOITHAU', 'TEN_GOITHAU', 'MA_TBMT', 'Ma_TBMT',
                   'MA_TBMT', 'Ma_TBMT', 'MA_TBMT', 'Ma_TBMT', 'Ma_TBMT']
    
    for sheet, header in zip(list_of_sheets, list_of_headers):
        dict_data[sheet].drop_duplicates(subset=header, keep='last', inplace=True, ignore_index=True)
    
    dict_mess = {
        'TBMT': TBMT_MOI_MESS_ALL,
        'GIA_HAN': GIA_HAN_MESS_ALL,
        'LAM_RO': LAM_RO_MESS_ALL,
        'KIEN_NGHI': KIEN_NGHI_MESS_ALL,
        'HUY_THAU': HUY_THAU_MESS_ALL,
        'OPENED_BID_1_MTHS': OPENED_BID_1_MTHS_MESS_ALL,
        'OPENED_DXKT': HOAN_THANH_MO_HSDXKT_MESS_ALL,
        'PUBLISH': OPEN_BID_PUBLISH_MESS_ALL,
        'APPROVED_DXKT': APPROVED_DXKT_MESS_ALL,
        'OPENED_DXTC': OPENED_DXTC_MESS_ALL
    }
    
    return dict_data, dict_mess