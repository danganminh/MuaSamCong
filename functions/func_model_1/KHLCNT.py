import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from functions.logic import convert_str_to_dtype, convert_MaDinhDanh_TenDonVi, get_value, wait_load

def get_IdGoiThau(link):
    return link.split('id=')[2].split('&')[0]

def get_planID(link):
    return link.split("notifyId=")[1].split("&")[0]


def prcessing_KHLCNT(driver, plan, madinhdanh, link):
    
    MaDinhDanh = []
    TenDonVi = []
    planID = []
    planNo = []
    planName = []
    planVersion = []
    planStatus = []
    TenDuToanMuaSam = []
    SoLuongGoiThau = []
    DuToanMuaSam = []
    CCY_DuToanMuaSam = []
    DuToanMuaSam_BangChu = []
    QD_KHLCNT_So = []
    QD_KHLCNT_Ngay = []
    QD_KHLCNT_NoiBanHanh = []
    #QD_KHLCNT_FileID = []
    QD_KHLCNT_FileName = []
    NgayDangTai_KHLCNT = []
    #PHANLOAI_KHLCNT = []
    MucTieuDauTu = []
    SuDungVonODA = []
    DiaDiemThucHien = []
    HinhThucQLDA = []
    NhomDuAn = []
    ThoiGianThucHienDuAn = []

    try:
        wait_load(driver, xpath='//*[@id="tab1"]/div/div/div/div', key='Mã KHLCNT')
        # ThongTinChung = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tender-notice"]/div/div/div[1]/div[1]/div[2]/ul/li[1]/a')))
        # ThongTinChung.click()
        # time.sleep(3)

        # Thông tin cơ bản
        planname = get_value(driver, key='Tên KHLCNT', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        planversion = get_value(driver, key='Phiên bản thay đổi', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        planstatus = get_value(driver, key='Trạng thái đăng tải', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        tendutoanmuasam = get_value(driver, key='Tên dự toán mua sắm', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        soluonggoithau = get_value(driver, key='Số lượng gói thầu', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        if soluonggoithau:
            soluonggoithau = convert_str_to_dtype(soluonggoithau, int)[0]
        
        muctieudautu = get_value(driver, key='Mục tiêu đầu tư', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        sudungvonODA = get_value(driver, key='Có sử dụng vốn ODA', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        diadiemthuchien = get_value(driver, key='Địa điểm thực hiện', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        hinhthucqlda = get_value(driver, key='Hình thức quản lý dự án', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        nhomduan = get_value(driver, key='Nhóm dự án', xpath_key='//*[@id="tab1"]/div[1]/div[2]')
        thoigianthuchienduan = get_value(driver, key='Thời gian thực hiện dự án', xpath_key='//*[@id="tab1"]/div[1]/div[2]')

        # Thông tin dự toán mua sắm
        dutoanmuasam = get_value(driver, key='Dự toán mua sắm', xpath_key='//*[@id="tab1"]/div[2]/div[2]')
        dutoanmuasam_float = None
        if dutoanmuasam:
            dutoanmuasam_float = convert_str_to_dtype(dutoanmuasam, float)[0]
            ccy_dutoanmuasam = dutoanmuasam.split()[-1]
        else:
            ccy_dutoanmuasam = None
        dutoanmuasam_bangchu = get_value(driver, key='Số tiền bằng chữ', xpath_key='//*[@id="tab1"]/div[2]/div[2]')

        # Thông tin quyết định phê duyệt
        qd_KHLCNT_so = get_value(driver, key='Số quyết định phê duyệt', xpath_key='//*[@id="tab1"]/div[3]/div[2]')
        qd_KHLCNT_ngay = get_value(driver, key='Ngày phê duyệt', xpath_key='//*[@id="tab1"]/div[3]/div[2]')
        qd_KHLCNT_noibanhanh = get_value(driver, key='Cơ quan ban hành quyết định', xpath_key='//*[@id="tab1"]/div[3]/div[2]')
        qd_KHLCNT_filename = get_value(driver, key='Quyết định phê duyệt', xpath_key='//*[@id="tab1"]/div[3]/div[2]')

        # Banner
        ngaydangtai_KHLCNT = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/p[3]'))).text

        # Append data
        MaDinhDanh.append(madinhdanh)
        TenDonVi.append(convert_MaDinhDanh_TenDonVi(madinhdanh))
        planNo.append(plan)
        planID.append(get_planID(link))
        planName.append(planname)
        planVersion.append(planversion)
        planStatus.append(planstatus)
        TenDuToanMuaSam.append(tendutoanmuasam)
        SoLuongGoiThau.append(soluonggoithau)
        MucTieuDauTu.append(muctieudautu)
        SuDungVonODA.append(sudungvonODA)
        DiaDiemThucHien.append(diadiemthuchien)
        HinhThucQLDA.append(hinhthucqlda)
        NhomDuAn.append(nhomduan)
        ThoiGianThucHienDuAn.append(thoigianthuchienduan)

        DuToanMuaSam.append(dutoanmuasam_float)
        CCY_DuToanMuaSam.append(ccy_dutoanmuasam)
        DuToanMuaSam_BangChu.append(dutoanmuasam_bangchu)

        QD_KHLCNT_So.append(qd_KHLCNT_so)
        QD_KHLCNT_Ngay.append(qd_KHLCNT_ngay)
        QD_KHLCNT_NoiBanHanh.append(qd_KHLCNT_noibanhanh)
        QD_KHLCNT_FileName.append(qd_KHLCNT_filename)
        NgayDangTai_KHLCNT.append(ngaydangtai_KHLCNT)

    except Exception as e:
        print(f'Error prcessing_KHLCNT as{str(e)}')
    

    data = {
        'MaDinhDanh': MaDinhDanh,
        'TenDonVi': TenDonVi,
        'planID': planID,
        'planNo': planNo,
        'planName': planName,
        'planVersion': planVersion,
        'planStatus': planStatus,
        'TenDuToanMuaSam': TenDuToanMuaSam,
        'SoLuongGoiThau': SoLuongGoiThau,
        'DuToanMuaSam': DuToanMuaSam,
        'CCY_DuToanMuaSam': CCY_DuToanMuaSam,
        'DuToanMuaSam_BangChu': DuToanMuaSam_BangChu,
        'QD_KHLCNT_So': QD_KHLCNT_So,
        'QD_KHLCNT_Ngay': QD_KHLCNT_Ngay,
        'QD_KHLCNT_NoiBanHanh': QD_KHLCNT_NoiBanHanh,
        #'QD_KHLCNT_FileID': QD_KHLCNT_FileID,
        'QD_KHLCNT_FileName': QD_KHLCNT_FileName,
        'NgayDangTai_KHLCNT': NgayDangTai_KHLCNT,
        #'PHANLOAI_KHLCNT': PHANLOAI_KHLCNT,
        'MucTieuDauTu': MucTieuDauTu,
        'SuDungVonODA': SuDungVonODA,
        'DiaDiemThucHien': DiaDiemThucHien,
        'HinhThucQLDA': HinhThucQLDA,
        'NhomDuAn': NhomDuAn,
        'ThoiGianThucHienDuAn': ThoiGianThucHienDuAn
    }

    # Print the length of each list
    print("\nLength of each list using for DEBUG KHLCNT:")
    for name, lst in data.items():
        print(f"{name}: {len(lst)}")
    
    df = pd.DataFrame(data)

    return df