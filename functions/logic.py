import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementClickInterceptedException

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


def convert_str_to_dtype(input_str, dtype):
    if input_str is None:
        return None
    result = []
    if isinstance(input_str, list):
        input_values = input_str
    else:
        input_values = input_str.split()
    for val in input_values:
        try:
            if '.' in val:
                val = val.replace('.', '')
            converted_val = dtype(val)
            result.append(converted_val)
        except ValueError:
            continue
    return result


def convert_MaDinhDanh_TenDonVi(MaDinhDanh):
    mapping = MAPPING_TENDONVI()
    for key, value in mapping.items():
        if key == MaDinhDanh:
            return value

def get_value(driver, key, xpath_key, time=10):
    result = None
    all_box = WebDriverWait(driver, time).until(EC.presence_of_all_elements_located((By.XPATH, f'{xpath_key}/div')))
    all_keys = WebDriverWait(driver, time).until(EC.presence_of_all_elements_located((By.XPATH, f'{xpath_key}/div/div')))
    for i in range(len(all_box)):
        for j in range(len(all_keys)):
            try:
                key_search = driver.find_element(By.XPATH, f'{xpath_key}/div[{i+1}]/div[{j+1}]')
                if key_search.text == key:
                    result = driver.find_element(By.XPATH, f'{xpath_key}/div[{i+1}]/div[{j+2}]')
                    result = result.text
                    return result
            except:
                continue
    return result


def wait_load(driver, xpath, key, loops=1000):
    print(f'Wait: {key}')
    for _ in range(loops):
        try:
            elem = driver.find_element(By.XPATH, xpath)
            if key in elem.text:
                print(f'wait pass {key}')
                break
        except:
            time.sleep(0.5)
            continue
        

def click_element(driver, xpath=None, loops=1000):
    for _ in range(loops):
        try:
            if xpath:
                driver.find_element(By.XPATH, xpath).click()
            else:
                driver.click()
            break
        except ElementClickInterceptedException:
            time.sleep(0.5)
            continue