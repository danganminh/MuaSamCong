import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from functions.logic import convert_str_to_dtype, convert_MaDinhDanh_TenDonVi, get_value, wait_load


home_page = 'https://muasamcong.mpi.gov.vn'
search_page = 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?render=search'


def get_IdGoiThau(link):
    return link.split('id=')[2].split('&')[0]


def processing_MaTBMT(driver, MaDinhDanh, planNo):
    def get_element_text(driver, xpath):
        try:
            return driver.find_element(By.XPATH, xpath).text
        except Exception:
            return None
    tengoithau = []
    gia_goithau = []
    ma_tbmt = []
    try:
        print(f'\n----- {MaDinhDanh}, {planNo} -----')
        TBMT_Box = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="tab2"]/div[1]/div/table/tbody/tr')))
        for i in range(len(TBMT_Box)):
            if len(TBMT_Box) > 1:
                xpath_tengoithau = f'//*[@id="tab2"]/div[1]/div/table/tbody/tr[{i+1}]/td[2]/a'
                xpath_gia_goithau = f'//*[@id="tab2"]/div[1]/div/table/tbody/tr[{i+1}]/td[4]/span'
                xpath_tbmt = f'//*[@id="tab2"]/div[1]/div/table/tbody/tr[{i+1}]/td[5]/span'
            else:
                xpath_tengoithau = '//*[@id="tab2"]/div[1]/div/table/tbody/tr/td[2]/a'
                xpath_gia_goithau = '//*[@id="tab2"]/div[1]/div/table/tbody/tr/td[4]/span'
                xpath_tbmt = '//*[@id="tab2"]/div[1]/div/table/tbody/tr/td[5]/span'
            tengoithau_val = get_element_text(driver, xpath_tengoithau)
            gia_goithau_val = get_element_text(driver, xpath_gia_goithau)
            tbmt_val = get_element_text(driver, xpath_tbmt)
            print(' ', tengoithau_val, gia_goithau_val, tbmt_val, sep='\n')
            tengoithau.append(tengoithau_val)
            gia_goithau.append(gia_goithau_val)
            ma_tbmt.append(tbmt_val)
    except NoSuchElementException:
        print('None TBMT')
    finally:
        return tengoithau, gia_goithau, ma_tbmt


def ID_and_sttTBMT(driver, TBMT):
    link_tbmt = []
    stt_tbmt = []
    try:
        for tbmt in TBMT:
            if tbmt is None:
                link_tbmt.append(None)
                stt_tbmt.append(None)
                continue                               
            # send tbmt to search page
            driver.get(home_page)
            # click KHLCNT
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/label[1]/span'))).click()
            driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/input').send_keys(tbmt)
            driver.find_element(By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/button').click()
            # add result
            link_detail = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]')))
            link = link_detail.find_element(By.TAG_NAME, 'a').get_attribute('href')
            stt = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[1]/span').text
            link_tbmt.append(link)
            stt_tbmt.append(stt)
    except Exception as e:
        print(f'Error ID_and_sttTBMT as {str(e)}')
    finally:
        return link_tbmt, stt_tbmt


def prcessing_GOI_THAU(driver, plan, madinhdanh, link):

    MaDinhDanh = []
    TenDonVi = []
    ID_GOITHAU = []
    planNo = []

    TEN_GOITHAU = []
    TRONGNUOC_QUOCTE = []
    HINHTHUC_DUTHAU = []
    LOAI_HOPDONG = []
    PHUONGTHUC_LCNT = []
    HINHTHUC_LCNT = []
    LINH_VUC = []
    GIA_GOITHAU = []
    CCY_GIA_GOITHAU = []
    PHAN_LO = []
    NGUON_VON = []
    THOIGIAN_THUCHIEN_HOPDONG = []
    NAM_BAOCAO = []
    TGIAN_BATDAU_TOCHUC_LCNT = []
    TGIAN_BATDAU_TOCHUC_LCNT_CHITIET = []
    MA_TBMT = []
    LINK_TBMT = []
    ID_TBMT = []
    STATUS_TBMT = []

    try:
        ThongTinGoiThau = driver.find_element(By.XPATH, '//*[@id="tender-notice"]/div/div/div[1]/div[1]/div[2]/ul/li[2]/a')
        ThongTinGoiThau.click()
        wait_load(driver, xpath='//*[@id="tab2"]/div[2]/div', key='Thông tin chi tiết gói thầu')
        
        trongnuoc_quocte = get_value(driver, key='Trong nước/ Quốc tế', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        hinhthuc_duthau = get_value(driver, key='Đấu thầu qua mạng', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        loai_hopdong = get_value(driver, key='Loại hợp đồng', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        phuongthuc_lcnt = get_value(driver, key='Phương thức LCNT', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        hinhthuc_lcnt = get_value(driver, key='Hình thức LCNT', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        linh_vuc = get_value(driver, key='Lĩnh vực', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        phan_lo = get_value(driver, key='Có nhiều phần/lô?', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        nguon_von = get_value(driver, key='Chi tiết nguồn vốn', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        thoigian_thuchien_hopdong = get_value(driver, key='Thời gian thực hiện hợp đồng', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        name_baocao = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/p[3]'))).text.split('/')[-1]
        tgian_batdau_tochuc_lcnt = get_value(driver, key='Thời gian bắt đầu tổ chức LCNT', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
        tgian_batdau_tochuc_lcnt_chitiet = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/p[3]')))
        tgian_batdau_tochuc_lcnt_chitiet = tgian_batdau_tochuc_lcnt_chitiet.text
        
        tengoithau, gia_goithau, ma_tbmt = processing_MaTBMT(driver, madinhdanh, plan)
        if tengoithau:
            link_tbmt, stt_tbmt = ID_and_sttTBMT(driver, ma_tbmt)
            TEN_GOITHAU.extend(tengoithau)
            MA_TBMT.extend(ma_tbmt)
            LINK_TBMT.extend(link_tbmt)
            STATUS_TBMT.extend(stt_tbmt)
            ID_TBMT.extend([link.split('&id=')[1].split('&')[0] if link else None for link in link_tbmt])
            if gia_goithau:
                gia_goithau_float = [convert_str_to_dtype(gia, float)[0] if gia else None for gia in gia_goithau]
                ccy_gia_goithau = [gia.split()[1].strip() if gia else None for gia in gia_goithau]
            else:
                gia_goithau_float = None
                ccy_gia_goithau = None
            GIA_GOITHAU.extend(gia_goithau_float)
            CCY_GIA_GOITHAU.extend(ccy_gia_goithau)
        else:
            # Append None values to all lists if no data is retrieved
            TEN_GOITHAU.append(None)
            MA_TBMT.append(None)
            LINK_TBMT.append(None)
            STATUS_TBMT.append(None)
            ID_TBMT.append(None)
            GIA_GOITHAU.append(None)
            CCY_GIA_GOITHAU.append(None)

        loop_add = len(ma_tbmt) if ma_tbmt is not None else 1

        for _ in range(loop_add):
            MaDinhDanh.append(madinhdanh)
            TenDonVi.append(convert_MaDinhDanh_TenDonVi(madinhdanh))
            ID_GOITHAU.append(get_IdGoiThau(link))
            planNo.append(plan)
            TRONGNUOC_QUOCTE.append(trongnuoc_quocte)
            HINHTHUC_DUTHAU.append(hinhthuc_duthau)
            LOAI_HOPDONG.append(loai_hopdong)
            PHUONGTHUC_LCNT.append(phuongthuc_lcnt)
            HINHTHUC_LCNT.append(hinhthuc_lcnt)
            LINH_VUC.append(linh_vuc)
            PHAN_LO.append(phan_lo)
            NGUON_VON.append(nguon_von)
            THOIGIAN_THUCHIEN_HOPDONG.append(thoigian_thuchien_hopdong)
            NAM_BAOCAO.append(name_baocao)
            TGIAN_BATDAU_TOCHUC_LCNT.append(tgian_batdau_tochuc_lcnt)
            TGIAN_BATDAU_TOCHUC_LCNT_CHITIET.append(tgian_batdau_tochuc_lcnt_chitiet)

    except Exception as e:
        print(f'Error get value GOI_THAU as {str(e)}')

    
    data = {
        'MaDinhDanh': MaDinhDanh,
        'TenDonVi': TenDonVi,
        'ID_GOITHAU': ID_GOITHAU,
        'planNo': planNo,
        'TEN_GOITHAU': TEN_GOITHAU,
        'TRONGNUOC_QUOCTE': TRONGNUOC_QUOCTE,
        'HINHTHUC_DUTHAU': HINHTHUC_DUTHAU,
        'LOAI_HOPDONG': LOAI_HOPDONG,
        'PHUONGTHUC_LCNT': PHUONGTHUC_LCNT,
        'HINHTHUC_LCNT': HINHTHUC_LCNT,
        'LINH_VUC': LINH_VUC,
        'GIA_GOITHAU': GIA_GOITHAU,
        'CCY_GIA_GOITHAU': CCY_GIA_GOITHAU,
        'PHAN_LO': PHAN_LO,
        'NGUON_VON': NGUON_VON,
        'THOIGIAN_THUCHIEN_HOPDONG': THOIGIAN_THUCHIEN_HOPDONG,
        'NAM_BAOCAO': NAM_BAOCAO,
        'TGIAN_BATDAU_TOCHUC_LCNT': TGIAN_BATDAU_TOCHUC_LCNT,
        'TGIAN_BATDAU_TOCHUC_LCNT_CHITIET': TGIAN_BATDAU_TOCHUC_LCNT_CHITIET,
        'MA_TBMT': MA_TBMT,
        'ID_TBMT': ID_TBMT,
        'STATUS_TBMT': STATUS_TBMT,
        'LINK_TBMT': LINK_TBMT
    }

    # Print the length of each list
    print("\nLength of each list using for DEBUG GOI_THAU:")
    for name, lst in data.items():
        print(f"{name}: {len(lst)}")

    df = pd.DataFrame(data)

    return df