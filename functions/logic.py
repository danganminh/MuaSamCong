import time
import requests
import pandas as pd
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


def Update_DataFrame(df_old, df_new, header_target):
    if df_old.empty or df_new.empty:
        return pd.concat([df_old, df_new], ignore_index=True)

    # Create a merged DataFrame that combines the information
    # Use 'header_target' as a key to match rows, and temporarily suffix the columns from df_new
    merged_df = pd.merge(df_old, df_new, on=header_target, how='left', suffixes=('', '_new'))

    # Replace the original values with new values if they are available
    for column in df_new.columns:
        if column in df_old.columns and column != header_target:  # make sure to exclude the header_target column
            merged_df[column] = merged_df[column + '_new'].combine_first(merged_df[column])

    # Drop the temporary new columns from the merge
    merged_df.drop(columns=[col for col in merged_df if col.endswith('_new')], inplace=True)

    return merged_df


def short_link(long_url):
    if not long_url:
        return None
    url = 'http://tinyurl.com/api-create.php?url='
    response = requests.get(url+long_url)
    return response.text


def MAPPING_TENDONVI():
    return {
            "vn5701662152": "1. Tổng công ty Phát điện 1",
            "vnz000009825": "9. Ban QLDA Nhiệt điện 3",
            "vnz000005052": "2. CTNĐ Uông Bí",
            "vnz000017073": "4. CTNĐ Duyên Hải",
            "vnz000005091": "3. CTNĐ Nghi Sơn",
            "vnz000023752": "5. CTTĐ Bản Vẽ",
            "vnz000013297": "6. CTTĐ Sông Tranh",
            "vnz000023738": "7. CTTĐ Đồng Nai",
            "vnz000016981": "8. CTTĐ Đại Ninh",
            "vn5800452036": "10. CTCP TĐ DHD",
            "vn5700434869": "11. CTCP NĐ Quảng Ninh",
            "vn0101264520": "12. VNPD",
            "vn0102379203": "13. EVNI",
            None: ""
        }


def MAPPING_STATUS_TBMT(STT_TBMT, HINHTHUC_LCNT):
    
    mapping = {
        'Chỉ định thầu': '00. Chỉ định thầu',
        'Chỉ định thầu rút gọn': '00. Chỉ định thầu rút gọn',
        'Đấu thầu hạn chế': '00. Đấu thầu hạn chế',
        'Lựa chọn nhà thầu trong trường hợp đặc biệt': '00. Lựa chọn nhà thầu trong trường hợp đặc biệt',
        'Mua sắm trực tiếp': '00. Mua sắm trực tiếp',
        'Tự thực hiện': '00. Tự thực hiện',
        'Chưa đóng thầu': '02. Chưa đóng thầu',
        'Chưa mở thầu': '02. Chưa mở thầu',
        'Đang xét thầu': '03. Đang xét thầu',
        'Có nhà thầu trúng thầu': '04. Có nhà thầu trúng thầu',
        'Không có nhà thầu trúng thầu': '05. Không có nhà thầu trúng thầu',
        'Đã hủy thầu': '06. Đã hủy thầu',
        'Đã huỷ thầu': '06. Đã hủy thầu',
        'Đã hủy Thông báo mời thầu': '07. Đã hủy TBMT',
        'Đã huỷ Thông báo mời thầu': '07. Đã hủy TBMT',
        'Đã hủy thông báo mời thầu': '07. Đã hủy TBMT',
        'Đã huỷ thông báo mời thầu': '07. Đã hủy TBMT',
        'Đã hủy TBMT': '07. Đã hủy TBMT',
        'Đã huỷ TBMT': '07. Đã hủy TBMT'
    }
    
    STT_TBMT = str(STT_TBMT)
    HINHTHUC_LCNT = str(HINHTHUC_LCNT)
    
    for key in mapping.keys():
        if STT_TBMT in key or HINHTHUC_LCNT in key:
            return mapping[key]
        
    return '01. Chưa có TBMT'


    

def convert_date_get_to_final_date(string_data):
    def convert_from_month(string_data):

        final_day_in_month = {
            'Tháng 1': '31',
            'Tháng 2': '28',
            'Tháng 3': '31',
            'Tháng 4': '30',
            'Tháng 5': '31',
            'Tháng 6': '30',
            'Tháng 7': '31',
            'Tháng 8': '31',
            'Tháng 9': '30',
            'Tháng 10': '31',
            'Tháng 11': '30',
            'Tháng 12': '31'
        }

        list_date = string_data.split(',')

        final_day = None
        month = None
        year = None

        for key, value in final_day_in_month.items():
            if key == list_date[0]:
                final_day = value
                break
        month_temp = list_date[0].split()[-1]
        if len(month_temp) == 1:
            month_temp = f'0{month_temp}'
        month = month_temp
        year = list_date[-1]

        return datetime.strptime(f'{final_day.strip()}/{month.strip()}/{year.strip()}', "%d/%m/%Y").date()

    mapping_Q = {
        'Quý I': 'Tháng 3',
        'Quý II': 'Tháng 6',
        'Quý III': 'Tháng 9',
        'Quý IV': 'Tháng 12'
    }
    
    result = None
    list_date = string_data.split(',')

    if 'Tháng' in list_date[0]:
        result = convert_from_month(string_data)

    elif 'Quý' in list_date[0]:
        month = None
        for key, value in mapping_Q.items():
            if key == list_date[0]:
                month = value
                break
        string_data = f'{month}, {list_date[-1]}'
        result = convert_from_month(string_data)
    
    return result


def convert_THAMQUYEN_PHEDUYET(TEN_DONVI, GIA_GOITHAU):
    THAMQUYEN_PHEDUYET = None
    if TEN_DONVI in ["4. CTNĐ Duyên Hải"]:
        if GIA_GOITHAU >= 15000000000:
            THAMQUYEN_PHEDUYET = "TCT"
        else:
            THAMQUYEN_PHEDUYET = "Đơn vị"
    elif TEN_DONVI in ["9. Ban QLDA Nhiệt điện 3", "2. CTNĐ Uông Bí", "3. CTNĐ Nghi Sơn"]:
        if GIA_GOITHAU >= 10000000000:
            THAMQUYEN_PHEDUYET = "TCT"
        else:
            THAMQUYEN_PHEDUYET = "Đơn vị"
    elif TEN_DONVI in ["5. CTTĐ Bản Vẽ", "6. CTTĐ Sông Tranh", "7. CTTĐ Đồng Nai", "8. CTTĐ Đại Ninh"]:
        if GIA_GOITHAU >= 5000000000:
            THAMQUYEN_PHEDUYET = "TCT"
        else:
            THAMQUYEN_PHEDUYET = "Đơn vị"
    elif TEN_DONVI in ["1. Tổng công ty Phát điện 1"]:
        THAMQUYEN_PHEDUYET = "TCT"
    else:
        THAMQUYEN_PHEDUYET = "Đơn vị"
    return THAMQUYEN_PHEDUYET


def convert_PHANLOAI_NGUONVON(NGUON_VON):
    nguon_von_mapping = {
        "SCL": ["SCL", "SỬA CHỮA LỚN"],
        "SXKD": ["SXKD", "SẢN XUẤT KINH DOANH"],
        "ĐTPT": ["ĐTPT", "ĐẦU TƯ PHÁT TRIỂN"],
        "ĐTXD": ["ĐTXD", "ĐẦU TƯ XÂY DỰNG"]
    }
    if not NGUON_VON: return None
    for key, value in nguon_von_mapping.items():
        for val in value:        
            if val in NGUON_VON.upper(): return key
    return None


def processing_STATUS_BID(driver, PHUONGTHUC_LCNT, STATUS_TBMT):
    list_section = ['Biên bản mở E-HSĐXKT', 'Biên bản mở E-HSDXKT', 'Danh sách nhà thầu đạt kỹ thuật', 'Biên bản mở E-HSĐXTC', 'Biên bản mở E-HSDXTC']
    if PHUONGTHUC_LCNT == 'Một giai đoạn một túi hồ sơ':
        if STATUS_TBMT == 'Chưa đóng thầu':
            return '"01'
        elif STATUS_TBMT == 'Đang xét thầu':
            return 'OPEN_BID'
        elif STATUS_TBMT == 'Có nhà thầu trúng thầu':
            return 'PUBLISH'
        return None
    elif PHUONGTHUC_LCNT == 'Một giai đoạn hai túi hồ sơ':
        if STATUS_TBMT == 'Chưa đóng thầu':
            return '"01'
        elif STATUS_TBMT == 'Đang xét thầu':
            father_section = driver.find_elements(By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li')
            for sec in father_section:
                if sec.text == list_section[0] or sec.text == list_section[1]:
                    return 'OPEN_DXTC'
                elif sec.text == list_section[2]:
                    return 'APPROVED_DXKT'
                elif sec.text == list_section[3] or sec.text == list_section[4]:
                    return 'OPENED_DXKT'
        elif STATUS_TBMT == 'Có nhà thầu trúng thầu':
            return 'PUBLISH'
        return None
    return None


def convert_str_to_dtype(input_str, dtype):
    if input_str is None or not isinstance(input_str, str):
        return [input_str]
    if input_str == '-':
        return [None]
    if isinstance(input_str, list):
        input_values = input_str
    else:
        if " " in input_str:
            input_values = input_str.split()
        else:
            input_values = [input_str]
    result = []
    for val in input_values:
        if '.' in val:
            val = val.replace('.', '')
        if ',' in val:
            val = val.replace(',', '.')
        try:
            converted_val = dtype(val)
            result.append(converted_val)
        except:
            continue
    return result


def convert_MaDinhDanh_TenDonVi(MaDinhDanh):
    mapping = MAPPING_TENDONVI()
    for key, value in mapping.items():
        if key == MaDinhDanh:
            return value


def get_value(driver, key, xpath_key, time=10):
    result = None
    try:
        all_keys = WebDriverWait(driver, time).until(EC.presence_of_all_elements_located((By.XPATH, f'{xpath_key}/div/div[1]')))
    except TimeoutException:
        return result
    for i in range(len(all_keys)):
        try:
            key_search = driver.find_element(By.XPATH, f'{xpath_key}/div[{i+1}]/div[1]')
            if key_search.text == key:
                result = driver.find_element(By.XPATH, f'{xpath_key}/div[{i+1}]/div[2]').text
                break
        except Exception:
            continue
    return result


def wait_load(driver, xpath, key, refresh=False):
    time.sleep(1)
    count = 0
    while True:
        try:
            if refresh and count >= 5:
                driver.refresh()
                time.sleep(5)
                count = 0
            elem = driver.find_element(By.XPATH, xpath)
            if key in elem.text:
                break
            count += 1
        except Exception:
            count += 1
            time.sleep(1)
            continue


def wait_dual_data(driver, xpath_left, xpath_right, sigma=1):
    time.sleep(1)
    while True:
        try:
            try:
                left = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, xpath_left)))
                right = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.XPATH, xpath_right)))
            except TimeoutException:
                time.sleep(1)
                continue
            if len(right) - sigma <= len(left) <= len(right) + sigma:
                break
            else:
                time.sleep(1)
                continue
        except Exception:
            time.sleep(1)
            continue


def click_wait(driver, xpath):
    while True:
        try:
            driver.find_element(By.XPATH, xpath).click()
            time.sleep(5)
            break
        except NoSuchElementException:
            time.sleep(1)
