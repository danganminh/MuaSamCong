import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from functions.logic import *
from functions.func_model_1.GIA_HAN import processing_GIA_HAN
from functions.func_model_1.KQChonNhaThau import processing_KQChonThau

home_page = 'https://muasamcong.mpi.gov.vn'
search_page = 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?render=search'


def processing_BienBanMoThau(driver):
    bbmt_so_nhathau_thamdu = thoi_diem_hoanthanh_mothau = None
    xpath_box = '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li'
    Box_info = driver.find_elements(By.XPATH, xpath_box)
    for i in range(len(Box_info)):
        box = driver.find_element(By.XPATH, f'{xpath_box}[{i+1}]')
        xpath_box_click = f'{xpath_box}[{i+1}]/a'
        if box.text == 'Biên bản mở thầu':
            click_wait(driver, xpath=xpath_box_click)
            wait_dual_data(driver, xpath_left='//*[@id="bidOpeningMinutes"]/div[1]/div[2]/div/div[1]', xpath_right='//*[@id="bidOpeningMinutes"]/div[1]/div[2]/div/div[2]')
            bbmt_so_nhathau_thamdu = get_value(driver, key='Tổng số nhà thầu tham dự', xpath_key='//*[@id="bidOpeningMinutes"]/div[1]/div[2]')
            thoi_diem_hoanthanh_mothau = get_value(driver, key='Thời điểm hoàn thành mở thầu', xpath_key='//*[@id="bidOpeningMinutes"]/div[1]/div[2]')
            break

    return bbmt_so_nhathau_thamdu, thoi_diem_hoanthanh_mothau
    

def processing_EHSDXKT(driver):
    def TongNhaThauThamDu(driver, xpath):
        all_elem = driver.find_elements(By.XPATH, xpath)
        for elem in all_elem:
            count = False
            for text in elem.text.split('\n'):
                if count:
                    return text
                if 'Tổng số nhà thầu tham dự' in text:
                    count = True
        return None
    
    bbmt_so_nhathau_thamdu = thoi_diem_hoanthanh_mothau = dutoan_goithau = None
    xpath_box = '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li'
    Box_info = driver.find_elements(By.XPATH, xpath_box)
    dont_have = True
    for i in range(len(Box_info)):
        box = driver.find_element(By.XPATH, f'{xpath_box}[{i+1}]')
        xpath_box_click = f'{xpath_box}[{i+1}]/a'
        if box.text == 'Biên bản mở E-HSDXKT' or box.text == 'Biên bản mở E-HSĐXKT':
            dont_have = False
            click_wait(driver, xpath=xpath_box_click)
            wait_dual_data(driver, xpath_left='//*[@id="hsdxkt"]/div[1]/div[2]/div/div[1]', xpath_right='//*[@id="hsdxkt"]/div[1]/div[2]/div/div[2]')
            bbmt_so_nhathau_thamdu = TongNhaThauThamDu(driver, '//*[@id="hsdxkt"]/div[1]/div[2]')
            thoi_diem_hoanthanh_mothau = get_value(driver, key='Thời điểm hoàn thành mở thầu', xpath_key='//*[@id="hsdxkt"]/div[1]/div[2]')
            dutoan_goithau = get_value(driver, key='Dự toán gói thầu', xpath_key='//*[@id="hsdxkt"]/div[1]/div[2]')
            if dutoan_goithau:
                dutoan_goithau = convert_str_to_dtype(dutoan_goithau, float)[0]
            break
    if dont_have:
        print('None Biên bản mở E-HSDXKT')

    return bbmt_so_nhathau_thamdu, thoi_diem_hoanthanh_mothau, dutoan_goithau


def processing_HSDXKT(driver):
    hsdxkt_so_qd = hsdxkt_ngay_qd = hsdxkt_noibanhanh_qd = hsdxkt_file_name = thoidiem_hoanthanh_mo_hsdxtc = None
    xpath_box = '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li'
    Box_info = driver.find_elements(By.XPATH, xpath_box)
    dont_have = True
    for i in range(len(Box_info)):
        box = driver.find_element(By.XPATH, f'{xpath_box}[{i+1}]')
        xpath_box_click = f'{xpath_box}[{i+1}]/a'
        if box.text == 'Danh sách nhà thầu đạt kỹ thuật':
            dont_have = False
            click_wait(driver, xpath=xpath_box_click)
            wait_dual_data(driver, xpath_left='//*[@id="tab3"]/div[2]/div[2]/div/div[1]', xpath_right='//*[@id="tab3"]/div[2]/div[2]/div/div[2]')
            hsdxkt_so_qd = get_value(driver, key='Số quyết định DS NT đạt kỹ thuật', xpath_key='//*[@id="tab3"]/div[2]/div[2]')
            hsdxkt_ngay_qd = get_value(driver, key='Ngày phê duyệt DS NT đạt kỹ thuật', xpath_key='//*[@id="tab3"]/div[2]/div[2]')
            hsdxkt_noibanhanh_qd = get_value(driver, key='Cơ quan ra quyết định phê duyệt DS NT đạt kỹ thuật', xpath_key='//*[@id="tab3"]/div[2]/div[2]')
            hsdxkt_file_name = get_value(driver, key='Quyết định phê duyệt DS NT đạt kỹ thuật', xpath_key='//*[@id="tab3"]/div[2]/div[2]')
            public_date = driver.find_element(By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[2]/div/div[1]/p[3]').text
            public_time = driver.find_element(By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[2]/div/div[1]/p[2]').text
            thoidiem_hoanthanh_mo_hsdxtc = f'{public_date} {public_time}'
            break
    if dont_have:
        print('None Danh sách nhà thầu đạt kỹ thuật')

    return hsdxkt_so_qd, hsdxkt_ngay_qd, hsdxkt_noibanhanh_qd, hsdxkt_file_name, thoidiem_hoanthanh_mo_hsdxtc
    

def processing_KetQuaChonThau(driver):
    kqcnt_df = pd.DataFrame()
    kqlcnt_so_qd = kqlcnt_ngay_qd = kqlcnt_noibanhanh_qd = kqlcnt_file_name = giatrungthau  = ngay_ky_hopdong = None
    xpath_box = '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/div[1]/div[2]/ul/li'
    Box_info = driver.find_elements(By.XPATH, xpath_box)
    dont_have = True
    for i in range(len(Box_info)):
        box = driver.find_element(By.XPATH, f'{xpath_box}[{i+1}]')
        xpath_box_click = f'{xpath_box}[{i+1}]/a'
        if box.text == 'Kết quả lựa chọn nhà thầu':
            dont_have = False
            click_wait(driver, xpath=xpath_box_click)
            wait_dual_data(driver, xpath_left='//*[@id="contractorSelectionResults"]/div[1]/div[2]/div/div[1]', xpath_right='//*[@id="contractorSelectionResults"]/div[1]/div[2]/div/div[2]')
            kqlcnt_so_qd = get_value(driver, key='Số quyết định phê duyệt', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
            kqlcnt_ngay_qd = get_value(driver, key='Ngày phê duyệt', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
            kqlcnt_noibanhanh_qd = get_value(driver, key='Bên mời thầu', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
            kqlcnt_file_name = get_value(driver, key='Quyết định phê duyệt', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
            try:
                kqcnt_df = processing_KQChonThau(driver, None, None)
                if not kqcnt_df.empty:
                    try:
                        giatrungthau = kqcnt_df.replace('nan', pd.NA).dropna(subset=['bidWiningPrice'])['bidWiningPrice'].values[-1]
                    except:
                        giatrungthau = None
                    try:
                        ngay_ky_hopdong = kqcnt_df.replace('nan', pd.NA).dropna(subset=['contractSignDate'])['contractSignDate'].values[-1]
                    except:
                        ngay_ky_hopdong= None
            except Exception as e:
                print(f'Error get table processing_KetQuaChonThau in GOI_THAU_CT as {str(e)}')
            break
    if dont_have:
        print('None Kết quả lựa chọn nhà thầu')

    return kqlcnt_so_qd, kqlcnt_ngay_qd, kqlcnt_noibanhanh_qd, kqlcnt_file_name, giatrungthau, ngay_ky_hopdong


def processing_HuyThau(driver):
    huythau_loai = huythau_so_qd = huythau_ngay_qd = huythau_noibanhanh_qd = huythau_file_name = huythau_ngay = huythau_reason = None 
    Box_Section = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="info-general"]/div')))
    dont_have = True
    for i in range(len(Box_Section) - 1): # Start as i+2 so end as len-1
        xpath_section = f'//*[@id="info-general"]/div[{i+2}]/div[1]'
        section = driver.find_element(By.XPATH, xpath_section)
        if 'Thông tin huỷ thầu' in section.text:
            dont_have = False
            huythau_so_qd = get_value(driver, key='Quyết định phê duyệt', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
            huythau_ngay_qd = get_value(driver, key='Ngày phê duyệt', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
            huythau_file_name = get_value(driver, key='Văn bản quyết định đính kèm', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
            huythau_ngay = get_value(driver, key='Thời điểm huỷ thầu', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
            huythau_reason = get_value(driver, key='Lý do hủy thầu', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
            break
    if dont_have:
        print('None Thông tin huỷ thầu')

    return huythau_loai, huythau_so_qd, huythau_ngay_qd, huythau_noibanhanh_qd, huythau_file_name, huythau_ngay, huythau_reason


def processing_GOI_THAU_CT(driver, data_base, index):
    
    tbmt_test = data_base['MA_TBMT'].values[index]
    
    print(f'Processing GOI_THAU_CT {tbmt_test}')

    GIA_HAN_DF = pd.DataFrame()
    
    # Thông báo mời thầu -> Thông tin chung
    #THAMQUYEN_PHEDUYET = []
    NGAYDANGTAI_TBMT = []
    PHIENBAN_THAYDOI = []
    THOIDIEM_MOTHAU = []
    THOIDIEM_DONGTHAU = []
    SOTIEN_DAMBAO_DUTHAU = []
    HINHTHUC_DAMBAO_DUTHAU = []
    HIEULUC_HSDT = []
    HSMT_SOQD = []
    HSMT_NGAYQD = []
    HSMT_NOIBANHANH = []
    HSMT_FILE_NAME = []
    #HSMT_FILE_ID = []

    # Thông báo mời thầu -> Thông tin chung -> Thông tin huỷ thông báo mời thầu
    HUYTHAU_LOAI = []
    HUYTHAU_SO_QD = []
    HUYTHAU_NGAY_QD = []
    HUYTHAU_NOIBANHANH_QD = []
    #HUYTHAU_FILE_ID = []
    HUYTHAU_FILE_NAME = []
    HUYTHAU_NGAY = []
    HUYTHAU_REASON = []

    # Biên bản mở E-HSDXKT
    DUTOAN_GOITHAU = []
    BBMT_SO_NHATHAU_THAMDU = []
    THOI_DIEM_HOANTHANH_MOTHAU = []
    
    # Danh sách nhà thầu đạt kỹ thuật
    HSDXKT_SO_QD = []
    HSDXKT_NGAY_QD = []
    HSDXKT_NOIBANHANH_QD = []
    #HSDXKT_FILE_ID = []
    HSDXKT_FILE_NAME = []
    THOIDIEM_HOANTHANH_MO_HSDXTC = []

    # Kết quả lựa chọn nhà thầu
    KQLCNT_SO_QD = []
    KQLCNT_NGAY_QD = []
    KQLCNT_NOIBANHANH_QD = []
    #KQLCNT_FILE_ID = []
    KQLCNT_FILE_NAME = []

    GIATRUNGTHAU = []
    NGAY_KY_HOPDONG = []
    #TYLE_TIETKIEM = []
    #THONGTIN_CHIALO = []

    # Click ThongTinChung
    click_wait(driver, xpath='//*[@id="tenderNotice"]/ul/li[1]/a')
    wait_dual_data(driver, xpath_left='//*[@id="info-general"]/div/div[2]/div/div[1]', xpath_right='//*[@id="info-general"]/div/div[2]/div/div[2]')
    
    # Check and add GIA_HAN value
    GIA_HAN_temp = processing_GIA_HAN(driver, data_base, index)
    if not GIA_HAN_temp.empty:
        GIA_HAN_DF = pd.concat([GIA_HAN_DF, GIA_HAN_temp], ignore_index=True)

    # Get values in Thông báo mời thầu -> Thông tin chung
    ngaydangtai_tbmt = get_value(driver, key='Ngày đăng tải', xpath_key='//*[@id="info-general"]/div[2]/div[2]')
    phienban_thaydoi = get_value(driver, key='Phiên bản thay đổi', xpath_key='//*[@id="info-general"]/div[2]/div[2]')
    if phienban_thaydoi and '\n' in phienban_thaydoi:
        phienban_thaydoi = phienban_thaydoi.split('\n')[-1]
    thoidiem_mothau = get_value(driver, key='Thời điểm mở thầu', xpath_key='//*[@id="info-general"]/div[6]/div[2]')
    thoidiem_dongthau = get_value(driver, key='Thời điểm đóng thầu', xpath_key='//*[@id="info-general"]/div[6]/div[2]')
    sotien_dambao_duthau = get_value(driver, key='Số tiền đảm bảo dự thầu', xpath_key='//*[@id="info-general"]/div[6]/div[2]')
    if sotien_dambao_duthau:
        sotien_dambao_duthau = convert_str_to_dtype(sotien_dambao_duthau, float)[0]
    hinhthuc_dambao_duthau = get_value(driver, key='Hình thức đảm bảo dự thầu', xpath_key='//*[@id="info-general"]/div[6]/div[2]')
    hieuluc_hsdt = get_value(driver, key='Hiệu lực hồ sơ dự thầu', xpath_key='//*[@id="info-general"]/div[6]/div[2]')
    hsmt_soqd = get_value(driver, key='Số quyết định phê duyệt', xpath_key='//*[@id="info-general"]/div[7]/div[2]')
    hsmt_ngayqd = get_value(driver, key='Ngày phê duyệt', xpath_key='//*[@id="info-general"]/div[7]/div[2]')
    hsmt_noibanhanh = get_value(driver, key='Cơ quan ban hành quyết định', xpath_key='//*[@id="info-general"]/div[7]/div[2]')
    hsmt_file_name = get_value(driver, key='Quyết định phê duyệt', xpath_key='//*[@id="info-general"]/div[7]/div[2]')

    # Append values
    NGAYDANGTAI_TBMT.append(ngaydangtai_tbmt)
    PHIENBAN_THAYDOI.append(phienban_thaydoi)
    THOIDIEM_MOTHAU.append(thoidiem_mothau)
    THOIDIEM_DONGTHAU.append(thoidiem_dongthau)
    SOTIEN_DAMBAO_DUTHAU.append(sotien_dambao_duthau)
    HINHTHUC_DAMBAO_DUTHAU.append(hinhthuc_dambao_duthau)
    HIEULUC_HSDT.append(hieuluc_hsdt)
    HSMT_SOQD.append(hsmt_soqd)
    HSMT_NGAYQD.append(hsmt_ngayqd)
    HSMT_NOIBANHANH.append(hsmt_noibanhanh)
    HSMT_FILE_NAME.append(hsmt_file_name)

    # Get values in Thông báo mời thầu -> Thông tin chung -> Thông tin huỷ thông báo mời thầu
    huythau_loai, huythau_so_qd, huythau_ngay_qd, huythau_noibanhanh_qd, huythau_file_name, huythau_ngay, huythau_reason = processing_HuyThau(driver)
    # Append values
    HUYTHAU_LOAI.append(huythau_loai)
    HUYTHAU_SO_QD.append(huythau_so_qd)
    HUYTHAU_NGAY_QD.append(huythau_ngay_qd)
    HUYTHAU_NOIBANHANH_QD.append(huythau_noibanhanh_qd)
    HUYTHAU_FILE_NAME.append(huythau_file_name)
    HUYTHAU_NGAY.append(huythau_ngay)
    HUYTHAU_REASON.append(huythau_reason)

    # Get values in Thông báo mời thầu -> Biên bản mở E-HSDXKT
    bbmt_so_nhathau_thamdu, thoi_diem_hoanthanh_mothau, dutoan_goithau = processing_EHSDXKT(driver)
    if not bbmt_so_nhathau_thamdu:
        bbmt_so_nhathau_thamdu, thoi_diem_hoanthanh_mothau = processing_BienBanMoThau(driver)
    # Append values
    BBMT_SO_NHATHAU_THAMDU.append(bbmt_so_nhathau_thamdu)
    THOI_DIEM_HOANTHANH_MOTHAU.append(thoi_diem_hoanthanh_mothau)
    DUTOAN_GOITHAU.append(dutoan_goithau)

    # Get values in Thông báo mời thầu -> Danh sách nhà thầu đạt kỹ thuật
    hsdxkt_so_qd, hsdxkt_ngay_qd, hsdxkt_noibanhanh_qd, hsdxkt_file_name, thoidiem_hoanthanh_mo_hsdxtc = processing_HSDXKT(driver)
    # Append values
    HSDXKT_SO_QD.append(hsdxkt_so_qd)
    HSDXKT_NGAY_QD.append(hsdxkt_ngay_qd)
    HSDXKT_NOIBANHANH_QD.append(hsdxkt_noibanhanh_qd)
    HSDXKT_FILE_NAME.append(hsdxkt_file_name)
    THOIDIEM_HOANTHANH_MO_HSDXTC.append(thoidiem_hoanthanh_mo_hsdxtc)

    # Kết quả lựa chọn nhà thầu
    kqlcnt_so_qd, kqlcnt_ngay_qd, kqlcnt_noibanhanh_qd, kqlcnt_file_name, giatrungthau, ngay_ky_hopdong = processing_KetQuaChonThau(driver)
    # Append values
    KQLCNT_SO_QD.append(kqlcnt_so_qd)
    KQLCNT_NGAY_QD.append(kqlcnt_ngay_qd)
    KQLCNT_NOIBANHANH_QD.append(kqlcnt_noibanhanh_qd)
    KQLCNT_FILE_NAME.append(kqlcnt_file_name)
    GIATRUNGTHAU.append(giatrungthau)
    NGAY_KY_HOPDONG.append(ngay_ky_hopdong)


    data = {
        'MaDinhDanh': [data_base['MaDinhDanh'].values[index]],
        'TenDonVi': [data_base['TenDonVi'].values[index]],
        'ID_GOITHAU': [data_base['ID_GOITHAU'].values[index]],
        'MA_TBMT': [data_base['MA_TBMT'].values[index]],
        'ID_TBMT': [data_base['ID_TBMT'].values[index]],
        'planNo': [data_base['planNo'].values[index]],
        'TEN_GOITHAU': [data_base['TEN_GOITHAU'].values[index]],
        'LINH_VUC': [data_base['LINH_VUC'].values[index]],
        'GIA_GOITHAU': [data_base['GIA_GOITHAU'].values[index]],
        'CCY_GIA_GOITHAU': [data_base['CCY_GIA_GOITHAU'].values[index]],
        'DUTOAN_GOITHAU': DUTOAN_GOITHAU,
        'NGUON_VON': [data_base['NGUON_VON'].values[index]],
        'PHANLOAI_NGUONVON': [convert_PHANLOAI_NGUONVON(NGUON_VON=data_base['NGUON_VON'].values[index])],
        'HINHTHUC_LCNT': [data_base['HINHTHUC_LCNT'].values[index]],
        'PHUONGTHUC_LCNT': [data_base['PHUONGTHUC_LCNT'].values[index]],
        'LOAI_HOPDONG': [data_base['LOAI_HOPDONG'].values[index]],
        'TRONGNUOC_QUOCTE': [data_base['TRONGNUOC_QUOCTE'].values[index]],
        'HINHTHUC_DUTHAU': [data_base['HINHTHUC_DUTHAU'].values[index]],
        'PHAN_LO': [data_base['PHAN_LO'].values[index]],
        'NAM_BAOCAO': [data_base['NAM_BAOCAO'].values[index]],
        'TGIAN_BATDAU_TOCHUC_LCNT': [data_base['TGIAN_BATDAU_TOCHUC_LCNT'].values[index]],
        'TGIAN_BATDAU_TOCHUC_LCNT_CHITIET': [data_base['TGIAN_BATDAU_TOCHUC_LCNT_CHITIET'].values[index]],
        'THOIGIAN_THUCHIEN_HOPDONG': [data_base['THOIGIAN_THUCHIEN_HOPDONG'].values[index]],
        'THAMQUYEN_PHEDUYET': [convert_THAMQUYEN_PHEDUYET(TEN_DONVI=data_base['TenDonVi'].values[index], GIA_GOITHAU=data_base['GIA_GOITHAU'].values[index])], #!!!
        'STATUS_TBMT': [data_base['STATUS_TBMT'].values[index]],
        'STATUS_BID': [processing_STATUS_BID(driver, PHUONGTHUC_LCNT=data_base['PHUONGTHUC_LCNT'].values[index], STATUS_TBMT=data_base['STATUS_TBMT'].values[index])], #!!!
        
        "MAPPING_STATUS_TBMT": [data_base['MAPPING_STATUS_TBMT'].values[index]],
        
        'NGAYDANGTAI_TBMT': [val if val else None for val in NGAYDANGTAI_TBMT],
        'PHIENBAN_THAYDOI': PHIENBAN_THAYDOI,
        'DIADIEM_PHATHANH_HSMT': ['https://muasamcong.mpi.gov.vn'], #!!!
        'DIADIEM_NHAN_HSMT': ['https://muasamcong.mpi.gov.vn'], #!!!
        'DIADIEM_MOTHAU': ['https://muasamcong.mpi.gov.vn'], #!!!
        'THOIDIEM_MOTHAU': THOIDIEM_MOTHAU,
        'THOIDIEM_DONGTHAU': THOIDIEM_DONGTHAU,
        'SOTIEN_DAMBAO_DUTHAU': SOTIEN_DAMBAO_DUTHAU,
        'HINHTHUC_DAMBAO_DUTHAU': HINHTHUC_DAMBAO_DUTHAU,
        'HIEULUC_HSDT': HIEULUC_HSDT,
        'HSMT_SOQD': HSMT_SOQD,
        'HSMT_NGAYQD': [val if val else None for val in HSMT_NGAYQD],
        'HSMT_NOIBANHANH': HSMT_NOIBANHANH,
        'HSMT_FILE_NAME': HSMT_FILE_NAME,
        'HSMT_FILE_ID': [None], #!!!
        'BBMT_SO_NHATHAU_THAMDU': BBMT_SO_NHATHAU_THAMDU,
        'THOI_DIEM_HOANTHANH_MOTHAU': [val if val else None for val in THOI_DIEM_HOANTHANH_MOTHAU],
        'HSDXKT_SO_QD': HSDXKT_SO_QD,
        'HSDXKT_NGAY_QD': [val if val else None for val in HSDXKT_NGAY_QD],
        'HSDXKT_NOIBANHANH_QD': HSDXKT_NOIBANHANH_QD,
        'HSDXKT_FILE_ID': [None], #!!!
        'HSDXKT_FILE_NAME': HSDXKT_FILE_NAME,
        'THOIDIEM_HOANTHANH_MO_HSDXTC': [val if val else None for val in THOIDIEM_HOANTHANH_MO_HSDXTC],

        # Dont need convert datatime type in here because, I do that in function
        # Kết quả lựa chọn nhà thầu
        'KQLCNT_SO_QD': KQLCNT_SO_QD,
        'KQLCNT_NGAY_QD': KQLCNT_NGAY_QD,
        'KQLCNT_NOIBANHANH_QD': KQLCNT_NOIBANHANH_QD,
        'KQLCNT_FILE_ID': [None], #!!!
        'KQLCNT_FILE_NAME': KQLCNT_FILE_NAME,

        'BCDG_HSDT_FILE_ID': [None], #!!!
        'BCDG_HSDT_FILE_NAME': HSMT_FILE_NAME,

        # Thông tin chung -> Thông tin huỷ thông báo mời thầu
        'HUYTHAU_LOAI': HUYTHAU_LOAI,
        'HUYTHAU_SO_QD': HUYTHAU_SO_QD,
        'HUYTHAU_NGAY_QD': HUYTHAU_NGAY_QD,
        'HUYTHAU_NOIBANHANH_QD': HUYTHAU_NOIBANHANH_QD,
        'HUYTHAU_FILE_ID': [None], #!!!
        'HUYTHAU_FILE_NAME': HUYTHAU_FILE_NAME,
        'HUYTHAU_NGAY': HUYTHAU_NGAY,
        'HUYTHAU_REASON': HUYTHAU_REASON,

        # Biên bản mở thầu -> Thông tin nhà thầu
        'GIATRUNGTHAU': GIATRUNGTHAU,
        'NGAY_KY_HOPDONG': NGAY_KY_HOPDONG,
        'TYLE_TIETKIEM': [None], #!!!
        'THONGTIN_CHIALO': [data_base['PHAN_LO'].values[index]],
        
        # Link add new
        'LINK': [driver.current_url]
    }

    GOI_THAU_CT_DF = pd.DataFrame(data)
    
    return GOI_THAU_CT_DF, GIA_HAN_DF