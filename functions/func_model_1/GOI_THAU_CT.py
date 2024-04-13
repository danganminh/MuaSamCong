import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from functions.logic import convert_str_to_dtype, get_value, wait_load, click_element
from functions.func_model_1.GIA_HAN import processing_GIA_HAN

home_page = 'https://muasamcong.mpi.gov.vn'
search_page = 'https://muasamcong.mpi.gov.vn/web/guest/contractor-selection?render=search'


def processing_EHSDXKT(driver):
    def processing_so_nhathau_thamdu(driver):
        try:
            box_xpath = '//*[@id="hsdxkt"]/div[1]/div[2]/div'
            box_section = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, box_xpath)))
            for i in range(len(box_section)):
                output_xpath = f'//*[@id="hsdxkt"]/div[1]/div[2]/div[{i+1}]'
                output_string = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, output_xpath))).text
                if 'Tổng số nhà thầu tham dự' in output_string:
                    result = int(output_string.split()[-1])
                    return result
        except Exception:
            print('None value so_nhathau_thamdu')
            return None
    bbmt_so_nhathau_thamdu = thoi_diem_hoanthanh_mothau = dutoan_goithau = None
    try:
        xpath_box = '//*[@id="tender-notice"]/div/div/div/div/div/div/div/ul/li'
        Box_info = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_box)))
        dont_have = True
        for box in Box_info:
            if box.text == 'Biên bản mở E-HSDXKT':
                dont_have = False
                click_element(box.find_element(By.XPATH, ".//a"))
                wait_load(driver, xpath='//*[@id="hsdxkt"]/div[1]/div', key='Biên bản mở thầu')
                bbmt_so_nhathau_thamdu = processing_so_nhathau_thamdu(driver)
                thoi_diem_hoanthanh_mothau = get_value(driver, key='Thời điểm hoàn thành mở thầu', xpath_key='//*[@id="hsdxkt"]/div[1]/div[2]')
                dutoan_goithau = get_value(driver, key='Dự toán gói thầu', xpath_key='//*[@id="hsdxkt"]/div[1]/div[2]')
                if dutoan_goithau:
                    dutoan_goithau = convert_str_to_dtype(dutoan_goithau, float)[0]
                break
        if dont_have:
            print('None Biên bản mở E-HSDXKT')
    except Exception as e:
        print(f'Error processing_EHSDXKT as {str(e)}')
    finally:
        return bbmt_so_nhathau_thamdu, thoi_diem_hoanthanh_mothau, dutoan_goithau


def processing_HSDXKT(driver):
    hsdxkt_so_qd = hsdxkt_ngay_qd = hsdxkt_noibanhanh_qd = hsdxkt_file_name = thoidiem_hoanthanh_mo_hsdxtc = None
    try:
        xpath_box = '//*[@id="tender-notice"]/div/div/div/div/div/div/div/ul/li'
        Box_info = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_box)))
        dont_have = True
        for box in Box_info:
            if box.text == 'Danh sách nhà thầu đạt kỹ thuật':
                dont_have = False
                click_element(box.find_element(By.XPATH, ".//a"))
                wait_load(driver, xpath='//*[@id="tab3"]/div[1]/div', key='Thông tin gói thầu')
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
    except Exception as e:
        print(f'Error processing_HSDXKT as {str(e)}')
    finally:
        return hsdxkt_so_qd, hsdxkt_ngay_qd, hsdxkt_noibanhanh_qd, hsdxkt_file_name, thoidiem_hoanthanh_mo_hsdxtc
    

def processing_KetQuaChonThau(driver):
    def get_value_giatrungthau(driver,):
        columns_1 = ['STT', 'Mã định danh', 'Tên nhà thầu', 'Giá dự thầu (VND)', 'Giá trúng thầu (VND)', 'Thời gian thực hiện hợp đồng']
        df_1 = pd.DataFrame(columns=columns_1)
        columns_2 = ["STT", "Mã định danh", "Tên nhà thầu", "Giá dự thầu (VND)", "Giá trúng thầu (VND)", "Thời gian giao hàng", "Thời gian giao hàng chi tiết"]
        df_2 = pd.DataFrame(columns=columns_2)
        KQChonThau = pd.DataFrame()
        data_1 = []
        data_2 = []
        try:
            section = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="contractorSelectionResults"]/div/div[1]')))
            for i, sec in enumerate(section):
                if sec.text == 'Thông tin Nhà thầu trúng thầu':
                    xpath_table = f'//*[@id="contractorSelectionResults"]/div[{i+1}]/div[2]/table'
                    try:
                        tbody = driver.find_element(By.XPATH, xpath_table)
                        for tr in tbody.find_elements(By.XPATH, '//tr'):
                            row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                            if len(row) == len(columns_1):
                                data_1.append(row)
                            elif len(row) == len(columns_2):
                                data_2.append(row)
                        break
                    except:
                        continue
            if data_1:
                for i in range(len(data_1)):
                    df_1.loc[i] = data_1[i]
            if data_2:
                for j in range(len(data_2)):
                    df_2.loc[j] = data_2[j]
            
            KQChonThau = pd.concat([df_1, df_2], ignore_index=True)
        except Exception as e:
            print(f'Error processing_KetQuaChonThau in Goi_Thau_CT as {str(e)}')
        finally:
            return KQChonThau

    def get_value_ngaykethopdong(driver):
        columns = ["STT", "Nhà thầu", "Ngày ký hợp đồng"]
        result = pd.DataFrame(columns=columns)
        data = []
        try:
            section = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="contractorSelectionResults"]/div/div[1]')))
            for i, sec in enumerate(section):
                if sec.text == 'Thông tin ký kết hợp đồng':
                    xpath_table = f'//*[@id="contractorSelectionResults"]/div[{i+1}]/div[2]/div/table' 
                    try:
                        tbody = driver.find_element(By.XPATH, xpath_table)
                        for tr in tbody.find_elements(By.XPATH, '//tr'):
                            row = [item.text for item in tr.find_elements(By.XPATH, './/td')]
                            if len(row) == len(columns):
                                if row[0] != '':
                                    data.append(row)
                        break
                    except:
                        continue
            
            for i in range(len(data)):
                result.loc[i] = data[i]

        except Exception as e:
            print(f'Error get_value_ngaykethopdong in Goi_Thau_CT as {str(e)}')
        finally:
            return result
        
    kqlcnt_so_qd = kqlcnt_ngay_qd = kqlcnt_noibanhanh_qd = kqlcnt_file_name = giatrungthau = ngay_ky_hopdong = giatrungthau = ngay_ky_hopdong = tyle_tietkiem = None
    try:
        xpath_box = '//*[@id="tender-notice"]/div/div/div/div/div/div/div/ul/li'
        Box_info = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, xpath_box)))
        dont_have = True
        for box in Box_info:
            if box.text == 'Kết quả lựa chọn nhà thầu':
                dont_have = False
                click_element(box.find_element(By.XPATH, ".//a"))
                wait_load(driver, xpath='//*[@id="contractorSelectionResults"]/div[1]/div', key='Thông tin gói thầu')
                kqlcnt_so_qd = get_value(driver, key='Số quyết định phê duyệt', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
                kqlcnt_ngay_qd = get_value(driver, key='Ngày phê duyệt', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
                kqlcnt_noibanhanh_qd = get_value(driver, key='Bên mời thầu', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
                kqlcnt_file_name = get_value(driver, key='Quyết định phê duyệt', xpath_key='//*[@id="contractorSelectionResults"]/div[1]/div[2]')
                giatrungthau = get_value_giatrungthau(driver).dropna()['Giá trúng thầu (VND)']
                if giatrungthau.empty:
                    giatrungthau = None
                else:
                    giatrungthau = giatrungthau.values
                ngay_ky_hopdong = get_value_ngaykethopdong(driver).dropna()['Ngày ký hợp đồng']
                if ngay_ky_hopdong.empty:
                    ngay_ky_hopdong = None  
                else:
                    ngay_ky_hopdong = ngay_ky_hopdong.values
                break
        if dont_have:
            print('None Kết quả lựa chọn nhà thầu')
    except Exception as e:
        print(f'Error KetQuaChonThau as {str(e)}')
    finally:
        return kqlcnt_so_qd, kqlcnt_ngay_qd, kqlcnt_noibanhanh_qd, kqlcnt_file_name, giatrungthau, ngay_ky_hopdong


def processing_HuyThau(driver):
    huythau_loai = huythau_so_qd = huythau_ngay_qd = huythau_noibanhanh_qd = huythau_file_name = huythau_ngay = huythau_reason = None 
    try:
        Box_Section = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="info-general"]/div')))
        dont_have = True
        for i in range(len(Box_Section) - 1): # Start as i+2 so end as len-1
            xpath_section = f'//*[@id="info-general"]/div[{i+2}]/div[1]'
            section = driver.find_element(By.XPATH, xpath_section)
            if 'huỷ' in section.text:
                dont_have = False
                huythau_so_qd = get_value(driver, key='Quyết định phê duyệt', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
                huythau_ngay_qd = get_value(driver, key='Ngày phê duyệt', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
                huythau_file_name = get_value(driver, key='Văn bản quyết định đính kèm', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
                huythau_ngay = get_value(driver, key='Thời điểm huỷ thông báo mời thầu', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
                huythau_reason = get_value(driver, key='Lý do huỷ thông báo mời thầu', xpath_key=f'//*[@id="info-general"]/div[{i+2}]/div[2]')
                break
        if dont_have:
            print('None Thông tin huỷ thầu')
    except Exception as e:
        print(f"Error processing_HuyThau as {str(e)}")
    finally:
        return huythau_loai, huythau_so_qd, huythau_ngay_qd, huythau_noibanhanh_qd, huythau_file_name, huythau_ngay, huythau_reason


def prcessing_GOI_THAU_CT(driver, data_base, index):
    
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
        
    try:
        ThongTinChung = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tenderNotice"]/ul/li[1]/a')))
        ThongTinChung.click()
        wait_load(driver, xpath='//*[@id="info-general"]/div[2]/div', key='Thông tin cơ bản')

        GIA_HAN_temp = processing_GIA_HAN(driver, data_base, index)
        if not GIA_HAN_temp.empty:
            GIA_HAN_DF = pd.concat([GIA_HAN_DF, GIA_HAN_temp], ignore_index=True)


        # Get values in Thông báo mời thầu -> Thông tin chung
        ngaydangtai_tbmt = get_value(driver, key='Ngày đăng tải', xpath_key='//*[@id="info-general"]/div[2]/div[2]')
        phienban_thaydoi = get_value(driver, key='Phiên bản thay đổi', xpath_key='//*[@id="info-general"]/div[2]/div[2]')
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

        if giatrungthau:
            giatrungthau = [convert_str_to_dtype(val, float)[0] if val else None for val in giatrungthau]
        GIATRUNGTHAU.append(giatrungthau)
        NGAY_KY_HOPDONG.append(ngay_ky_hopdong)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    
    
    data = {
        'MaDinhDanh': data_base['MaDinhDanh'].iloc[[index]],
        'TenDonVi': data_base['TenDonVi'].iloc[[index]],
        'ID_GOITHAU': data_base['ID_GOITHAU'].iloc[[index]],
        'MA_TBMT': data_base['MA_TBMT'].iloc[[index]],
        'ID_TBMT': data_base['ID_TBMT'].iloc[[index]],
        'planNo': data_base['planNo'].iloc[[index]],
        'TEN_GOITHAU': data_base['TEN_GOITHAU'].iloc[[index]],
        'LINH_VUC': data_base['LINH_VUC'].iloc[[index]],
        'GIA_GOITHAU': data_base['GIA_GOITHAU'].iloc[[index]],
        'CCY_GIA_GOITHAU': data_base['CCY_GIA_GOITHAU'].iloc[[index]],
        'DUTOAN_GOITHAU': DUTOAN_GOITHAU,
        'NGUON_VON': data_base['NGUON_VON'].iloc[[index]],
        'HINHTHUC_LCNT': data_base['HINHTHUC_LCNT'].iloc[[index]],
        'PHUONGTHUC_LCNT': data_base['PHUONGTHUC_LCNT'].iloc[[index]],
        'LOAI_HOPDONG': data_base['LOAI_HOPDONG'].iloc[[index]],
        'TRONGNUOC_QUOCTE': data_base['TRONGNUOC_QUOCTE'].iloc[[index]],
        'HINHTHUC_DUTHAU': data_base['HINHTHUC_DUTHAU'].iloc[[index]],
        'PHAN_LO': data_base['PHAN_LO'].iloc[[index]],
        'NAM_BAOCAO': data_base['NAM_BAOCAO'].iloc[[index]],
        'TGIAN_BATDAU_TOCHUC_LCNT': data_base['TGIAN_BATDAU_TOCHUC_LCNT'].iloc[[index]],
        'TGIAN_BATDAU_TOCHUC_LCNT_CHITIET': data_base['TGIAN_BATDAU_TOCHUC_LCNT_CHITIET'].iloc[[index]],
        'THOIGIAN_THUCHIEN_HOPDONG': data_base['THOIGIAN_THUCHIEN_HOPDONG'].iloc[[index]],
        #'THAMQUYEN_PHEDUYET': loading,
        'STATUS_TBMT': data_base['STATUS_TBMT'].iloc[[index]],
        'NGAYDANGTAI_TBMT': NGAYDANGTAI_TBMT,
        'PHIENBAN_THAYDOI': PHIENBAN_THAYDOI,
        'THOIDIEM_MOTHAU': THOIDIEM_MOTHAU,
        'THOIDIEM_DONGTHAU': THOIDIEM_DONGTHAU,
        'SOTIEN_DAMBAO_DUTHAU': SOTIEN_DAMBAO_DUTHAU,
        'HINHTHUC_DAMBAO_DUTHAU': HINHTHUC_DAMBAO_DUTHAU,
        'HIEULUC_HSDT': HIEULUC_HSDT,
        'HSMT_SOQD': HSMT_SOQD,
        'HSMT_NGAYQD': HSMT_NGAYQD,
        'HSMT_NOIBANHANH': HSMT_NOIBANHANH,
        'HSMT_FILE_NAME': HSMT_FILE_NAME,
        #'HSMT_FILE_ID': loading,
        'BBMT_SO_NHATHAU_THAMDU': BBMT_SO_NHATHAU_THAMDU,
        'THOI_DIEM_HOANTHANH_MOTHAU': THOI_DIEM_HOANTHANH_MOTHAU,
        'HSDXKT_SO_QD': HSDXKT_SO_QD,
        'HSDXKT_NGAY_QD': HSDXKT_NGAY_QD,
        'HSDXKT_NOIBANHANH_QD': HSDXKT_NOIBANHANH_QD,
        #'HSDXKT_FILE_ID': loading,
        'HSDXKT_FILE_NAME': HSDXKT_FILE_NAME,
        'THOIDIEM_HOANTHANH_MO_HSDXTC': THOIDIEM_HOANTHANH_MO_HSDXTC,

        # Kết quả lựa chọn nhà thầu
        'KQLCNT_SO_QD': KQLCNT_SO_QD,
        'KQLCNT_NGAY_QD': KQLCNT_NGAY_QD,
        'KQLCNT_NOIBANHANH_QD': KQLCNT_NOIBANHANH_QD,
        #'KQLCNT_FILE_ID': loading,
        'KQLCNT_FILE_NAME': KQLCNT_FILE_NAME,

        #'BCDG_HSDT_FILE_ID': loading,
        'BCDG_HSDT_FILE_NAME': HSMT_FILE_NAME,

        # Thông tin chung -> Thông tin huỷ thông báo mời thầu
        'HUYTHAU_LOAI': HUYTHAU_LOAI,
        'HUYTHAU_SO_QD': HUYTHAU_SO_QD,
        'HUYTHAU_NGAY_QD': HUYTHAU_NGAY_QD,
        'HUYTHAU_NOIBANHANH_QD': HUYTHAU_NOIBANHANH_QD,
        #'HUYTHAU_FILE_ID': loading,
        'HUYTHAU_FILE_NAME': HUYTHAU_FILE_NAME,
        'HUYTHAU_NGAY': HUYTHAU_NGAY,
        'HUYTHAU_REASON': HUYTHAU_REASON,

        # Biên bản mở thầu -> Thông tin nhà thầu
        'GIATRUNGTHAU': GIATRUNGTHAU,
        'NGAY_KY_HOPDONG': NGAY_KY_HOPDONG,
        #'TYLE_TIETKIEM': loading,
        'THONGTIN_CHIALO': data_base['PHAN_LO'].iloc[[index]]
    }

    # Print the length of each list
    print("\nLength of each list using for DEBUG GOI_THAU_CT:")
    for name, lst in data.items():
        print(f"{name}: {len(lst)}")

    GOI_THAU_CT_DF = pd.DataFrame(data)

    return GOI_THAU_CT_DF, GIA_HAN_DF