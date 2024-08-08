import time
import numpy as np
import pandas as pd
from io import StringIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from functions.logic import *

home_page = 'https://muasamcong.mpi.gov.vn'

def get_IdGoiThau(data_base, planNo_now, len_df_now):
    od_id = data_base['ID_GOITHAU'].values
    result = []
    for i in range(len_df_now):
        while True:
            num = ''.join([str(np.random.randint(0, 10)) for _ in range(3)])
            new_id = f'{planNo_now}_{num}'
            if new_id not in od_id and new_id not in result:
                result.append(new_id)
                break
    return result


def processing_MaTBMT(driver):
    columns = ["STT", "Tên gói thầu", "Dự toán gói thầu được duyệt sau khi phê duyệt KHLCNT", "Giá gói thầu", "Số thông báo liên kết"]
    df = pd.DataFrame(columns=columns)
    data = []    
    # Find table
    all_table = pd.read_html(StringIO(driver.page_source))
    for table in all_table:
        try:
            if len(table.columns) == len(columns) and all(table.columns == columns):
                data = table.values.tolist()
        except:
            continue
    for i in range(len(data)):
        df.loc[i] = data[i]
    
    tengoithau = df["Tên gói thầu"].values
    gia_goithau = df["Giá gói thầu"].values
    ma_tbmt = df["Số thông báo liên kết"].values
    
    return tengoithau, gia_goithau, ma_tbmt


def processing_GOI_THAU_Update_module2(driver, STT_NEW, data_original, index):
    
    wait_dual_data(driver, xpath_left='//*[@id="info-general"]/div/div[2]/div/div[1]', xpath_right='//*[@id="info-general"]/div/div[2]/div/div[2]')
    
    TBMT = get_value(driver, key='Mã TBMT', xpath_key='//*[@id="info-general"]/div[2]/div[2]')
            
    print(f'Processing GOI_THAU_Update_module2 {TBMT}, {STT_NEW}')

    madinhdanh = data_original['MaDinhDanh'].values[index]
    plan = data_original['planNo'].values[index]
    ten = data_original['TEN_GOITHAU'].values[index]
    gia_goithau_float = data_original['GIA_GOITHAU'].values[index]
    ccy_gia_goithau = data_original['CCY_GIA_GOITHAU'].values[index]
    phan_lo = data_original['PHAN_LO'].values[index]
    tgian_batdau_tochuc_lcnt = data_original['TGIAN_BATDAU_TOCHUC_LCNT'].values[index]
    id_goithau = data_original['ID_GOITHAU'].values[index]
    
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
    #TGIAN_BATDAU_TOCHUC_LCNT_CHITIET = []
    MA_TBMT = []
    ID_TBMT = []
    STATUS_TBMT = []

    # Add None
    planID = []
    STATUS_BID = []
    linkNotifyInfo = []
    numBidderJoin = []
    bidRealityOpenDate = []
    PHANLOAI_NGUONVON = []
    THAMQUYEN_PHEDUYET = []
    ACTION = []
        
    # Section Thông tin gói thầu
    trongnuoc_quocte = get_value(driver, key='Trong nước/ Quốc tế', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
    loai_hopdong = get_value(driver, key='Loại hợp đồng', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
    linh_vuc = get_value(driver, key='Lĩnh vực', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
    phuongthuc_lcnt = get_value(driver, key='Phương thức lựa chọn nhà thầu', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
    nguon_von = get_value(driver, key='Chi tiết nguồn vốn', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
    thoigian_thuchien_hopdong = get_value(driver, key='Thời gian thực hiện hợp đồng', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
    hinhthuc_lcnt = get_value(driver, key='Hình thức lựa chọn nhà thầu', xpath_key='//*[@id="info-general"]/div[4]/div[2]')

    # Cách thức dự thầu
    hinhthuc_duthau = get_value(driver, key='Hình thức dự thầu', xpath_key='//*[@id="info-general"]/div[5]/div[2]')
    name_baocao = driver.find_element(By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[2]/div/div[1]/p[3]').text.split('/')[-1]

    # Append data
    MaDinhDanh.append(madinhdanh)
    TenDonVi.append(convert_MaDinhDanh_TenDonVi(madinhdanh))
    
    ID_GOITHAU.append(id_goithau)
    
    planNo.append(plan)
    TEN_GOITHAU.append(ten)
    TRONGNUOC_QUOCTE.append(trongnuoc_quocte)
    HINHTHUC_DUTHAU.append(hinhthuc_duthau)
    LOAI_HOPDONG.append(loai_hopdong)
    PHUONGTHUC_LCNT.append(phuongthuc_lcnt)
    HINHTHUC_LCNT.append(hinhthuc_lcnt)
    LINH_VUC.append(linh_vuc)
    
    GIA_GOITHAU.append(gia_goithau_float)
    CCY_GIA_GOITHAU.append(ccy_gia_goithau)

    PHAN_LO.append(phan_lo)
    NGUON_VON.append(nguon_von)
    THOIGIAN_THUCHIEN_HOPDONG.append(thoigian_thuchien_hopdong)
    NAM_BAOCAO.append(name_baocao)
    TGIAN_BATDAU_TOCHUC_LCNT.append(tgian_batdau_tochuc_lcnt)

    MA_TBMT.append(TBMT)
    ID_TBMT.append(driver.current_url.split('&id=')[1].split('&')[0])

    STATUS_TBMT.append(STT_NEW)

    # PHAN_LOAI_NGUON_VON
    phanloai_nguonvon = convert_PHANLOAI_NGUONVON(NGUON_VON=nguon_von)
    PHANLOAI_NGUONVON.append(phanloai_nguonvon)
    # convert_THAMQUYEN_PHEDUYET
    thamquyen_pheduyet = convert_THAMQUYEN_PHEDUYET(TEN_DONVI=convert_MaDinhDanh_TenDonVi(madinhdanh), GIA_GOITHAU=gia_goithau_float)
    THAMQUYEN_PHEDUYET.append(thamquyen_pheduyet)
    # processing_STATUS_BID
    status_bid = processing_STATUS_BID(driver, PHUONGTHUC_LCNT=phuongthuc_lcnt, STATUS_TBMT=STT_NEW)
    STATUS_BID.append(status_bid)

    linkNotifyInfo.append(None)
    numBidderJoin.append(None)
    bidRealityOpenDate.append(None)
    ACTION.append(None)
    planID.append(None)

    data = {
        'MaDinhDanh': MaDinhDanh,
        'TenDonVi': TenDonVi,
        'ID_GOITHAU': [None for _ in range(len(MaDinhDanh))], # Append later
        'planNo': planNo,
        'planID': planID,
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
        'TGIAN_BATDAU_TOCHUC_LCNT_CHITIET': [convert_date_get_to_final_date(val) if val else None for val in TGIAN_BATDAU_TOCHUC_LCNT],
        'MA_TBMT': MA_TBMT,
        'ID_TBMT': ID_TBMT,

        'STATUS_TBMT': STATUS_TBMT,
        "STATUS_BID": STATUS_BID,
        
        "MAPPING_STATUS_TBMT": [MAPPING_STATUS_TBMT(STT_TBMT=val_1, HINHTHUC_LCNT=val_2) for val_1, val_2 in zip(STATUS_TBMT, HINHTHUC_LCNT)],

        "linkNotifyInfo": linkNotifyInfo,
        "numBidderJoin": numBidderJoin,
        "bidRealityOpenDate": bidRealityOpenDate,
        "PHANLOAI_NGUONVON": PHANLOAI_NGUONVON,
        "THAMQUYEN_PHEDUYET": THAMQUYEN_PHEDUYET,
        "ACTION": ACTION,

    }
        
    GOI_THAU_NEW = pd.DataFrame(data)
    
    return GOI_THAU_NEW


def processing_GOI_THAU(driver, plan, madinhdanh, data_base):

    print(f'Processing GOI_THAU {plan}, {madinhdanh}')

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
    #TGIAN_BATDAU_TOCHUC_LCNT_CHITIET = []
    MA_TBMT = []
    ID_TBMT = []
    STATUS_TBMT = []

    # Add None
    planID = []
    STATUS_BID = []
    linkNotifyInfo = []
    numBidderJoin = []
    bidRealityOpenDate = []
    PHANLOAI_NGUONVON = []
    THAMQUYEN_PHEDUYET = []
    ACTION = []

    # Click ThongTinGoiThau
    click_wait(driver, xpath='//*[@id="tender-notice"]/div/div/div[1]/div[1]/div[2]/ul/li[2]/a')
    wait_dual_data(driver, xpath_left='//*[@id="tab2"]/div[2]/div[2]/div/div[1]', xpath_right='//*[@id="tab2"]/div[2]/div[2]/div/div[2]')

    trongnuoc_quocte_PL = get_value(driver, key='Trong nước/ Quốc tế', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    hinhthuc_duthau_PL = get_value(driver, key='Đấu thầu qua mạng', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    loai_hopdong_PL = get_value(driver, key='Loại hợp đồng', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    phuongthuc_lcnt_PL = get_value(driver, key='Phương thức LCNT', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    hinhthuc_lcnt_PL = get_value(driver, key='Hình thức LCNT', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    linh_vuc_PL = get_value(driver, key='Lĩnh vực', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    phan_lo_PL = get_value(driver, key='Có nhiều phần/lô?', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    nguon_von_PL = get_value(driver, key='Chi tiết nguồn vốn', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    thoigian_thuchien_hopdong_PL = get_value(driver, key='Thời gian thực hiện hợp đồng', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    name_baocao_PL = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[1]/p[3]'))).text.split('/')[-1]
    tgian_batdau_tochuc_lcnt_PL = get_value(driver, key='Thời gian bắt đầu tổ chức LCNT', xpath_key='//*[@id="tab2"]/div[2]/div[2]')
    tengoithau, gia_goithau, ma_tbmt = processing_MaTBMT(driver)
    
    
    # Search Step by Step with ma_tbmt
    for tbmt, ten, gia in zip(ma_tbmt, tengoithau, gia_goithau):
        
        gia_goithau_float = None
        ccy_gia_goithau = None

        if gia:
            gia_goithau_float = convert_str_to_dtype(gia, float)[0]
            ccy_gia_goithau = gia.split()[-1].strip()
            
        if pd.isna(tbmt):
            MaDinhDanh.append(madinhdanh)
            TenDonVi.append(convert_MaDinhDanh_TenDonVi(madinhdanh))
            planNo.append(plan)
            TEN_GOITHAU.append(ten)
            TRONGNUOC_QUOCTE.append(trongnuoc_quocte_PL)
            HINHTHUC_DUTHAU.append(hinhthuc_duthau_PL)
            LOAI_HOPDONG.append(loai_hopdong_PL)
            PHUONGTHUC_LCNT.append(phuongthuc_lcnt_PL)
            HINHTHUC_LCNT.append(hinhthuc_lcnt_PL)
            LINH_VUC.append(linh_vuc_PL)
            
            GIA_GOITHAU.append(gia_goithau_float)
            CCY_GIA_GOITHAU.append(ccy_gia_goithau)

            PHAN_LO.append(phan_lo_PL)
            NGUON_VON.append(nguon_von_PL)
            THOIGIAN_THUCHIEN_HOPDONG.append(thoigian_thuchien_hopdong_PL)
            NAM_BAOCAO.append(name_baocao_PL)
            TGIAN_BATDAU_TOCHUC_LCNT.append(tgian_batdau_tochuc_lcnt_PL)

            MA_TBMT.append(None)
            ID_TBMT.append(None)
            STATUS_TBMT.append(None)

            # convert_PHANLOAI_NGUONVON
            phanloai_nguonvon_PL = convert_PHANLOAI_NGUONVON(NGUON_VON=nguon_von_PL)
            PHANLOAI_NGUONVON.append(phanloai_nguonvon_PL)
            # convert_THAMQUYEN_PHEDUYET
            thamquyen_pheduyet_PL = convert_THAMQUYEN_PHEDUYET(TEN_DONVI=convert_MaDinhDanh_TenDonVi(madinhdanh), GIA_GOITHAU=gia_goithau_float)
            THAMQUYEN_PHEDUYET.append(thamquyen_pheduyet_PL)
            # processing_STATUS_BID
            status_bid_PL = processing_STATUS_BID(driver, PHUONGTHUC_LCNT=phuongthuc_lcnt_PL, STATUS_TBMT=None)
            STATUS_BID.append(status_bid_PL)
            
            linkNotifyInfo.append(None)
            numBidderJoin.append(None)
            bidRealityOpenDate.append(None)
            ACTION.append(None)
            planID.append(None)
            continue
        
        # send tbmt to search page
        driver.get(home_page)
        wait_load(driver, xpath='//*[@id="home"]/div/div/div/div', key='Tìm kiếm thông tin đấu thầu')
        # click KHLCNT
        KHLCNT_method = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[3]/div[1]/div[1]/label[1]/span'))
        )
        KHLCNT_method.click()
        time.sleep(1)
        box_search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/input'))
        )
        box_search.send_keys(tbmt)
        time.sleep(1)
        search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div/div[1]/div[2]/div[2]/div/button'))
        )
        search_button.click()
        # add result
        wait_load(driver, xpath='//*[@id="search-home"]/div/div/div/div/div/label', key='kết quả')
        stt = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[1]/span').text
        
        # Get TBMT page
        link_detail = driver.find_element(By.XPATH, '//*[@id="bid-closed"]/div/div/div[2]/div[1]')
        driver.get(link_detail.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        wait_dual_data(driver, xpath_left='//*[@id="info-general"]/div/div[2]/div/div[1]', xpath_right='//*[@id="info-general"]/div/div[2]/div/div[2]')

        # Get crawl data
        # Section Thông tin gói thầu
        trongnuoc_quocte = get_value(driver, key='Trong nước/ Quốc tế', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
        loai_hopdong = get_value(driver, key='Loại hợp đồng', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
        linh_vuc = get_value(driver, key='Lĩnh vực', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
        phuongthuc_lcnt = get_value(driver, key='Phương thức lựa chọn nhà thầu', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
        nguon_von = get_value(driver, key='Chi tiết nguồn vốn', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
        thoigian_thuchien_hopdong = get_value(driver, key='Thời gian thực hiện hợp đồng', xpath_key='//*[@id="info-general"]/div[4]/div[2]')
        hinhthuc_lcnt = get_value(driver, key='Hình thức lựa chọn nhà thầu', xpath_key='//*[@id="info-general"]/div[4]/div[2]')

        # Cách thức dự thầu
        hinhthuc_duthau = get_value(driver, key='Hình thức dự thầu', xpath_key='//*[@id="info-general"]/div[5]/div[2]')
        phan_lo = phan_lo_PL
        name_baocao = driver.find_element(By.XPATH, '//*[@id="tender-notice"]/div/div/div[2]/div/div[2]/div/div[1]/p[3]').text.split('/')[-1]
        tgian_batdau_tochuc_lcnt = tgian_batdau_tochuc_lcnt_PL

        # Append data
        MaDinhDanh.append(madinhdanh)
        TenDonVi.append(convert_MaDinhDanh_TenDonVi(madinhdanh))
                
        planNo.append(plan)
        TEN_GOITHAU.append(ten)
        TRONGNUOC_QUOCTE.append(trongnuoc_quocte)
        HINHTHUC_DUTHAU.append(hinhthuc_duthau)
        LOAI_HOPDONG.append(loai_hopdong)
        PHUONGTHUC_LCNT.append(phuongthuc_lcnt)
        HINHTHUC_LCNT.append(hinhthuc_lcnt)
        LINH_VUC.append(linh_vuc)
        
        GIA_GOITHAU.append(gia_goithau_float)
        CCY_GIA_GOITHAU.append(ccy_gia_goithau)

        PHAN_LO.append(phan_lo)
        NGUON_VON.append(nguon_von)
        THOIGIAN_THUCHIEN_HOPDONG.append(thoigian_thuchien_hopdong)
        NAM_BAOCAO.append(name_baocao)
        TGIAN_BATDAU_TOCHUC_LCNT.append(tgian_batdau_tochuc_lcnt)

        MA_TBMT.append(tbmt)
        ID_TBMT.append(driver.current_url.split('&id=')[1].split('&')[0])

        STATUS_TBMT.append(stt)

        # PHAN_LOAI_NGUON_VON
        phanloai_nguonvon = convert_PHANLOAI_NGUONVON(NGUON_VON=nguon_von)
        PHANLOAI_NGUONVON.append(phanloai_nguonvon)
        # convert_THAMQUYEN_PHEDUYET
        thamquyen_pheduyet = convert_THAMQUYEN_PHEDUYET(TEN_DONVI=convert_MaDinhDanh_TenDonVi(madinhdanh), GIA_GOITHAU=gia_goithau_float)
        THAMQUYEN_PHEDUYET.append(thamquyen_pheduyet)
        # processing_STATUS_BID
        status_bid = processing_STATUS_BID(driver, PHUONGTHUC_LCNT=phuongthuc_lcnt, STATUS_TBMT=stt)
        STATUS_BID.append(status_bid)

        linkNotifyInfo.append(None)
        numBidderJoin.append(None)
        bidRealityOpenDate.append(None)
        ACTION.append(None)
        planID.append(None)


        
    data = {
        'MaDinhDanh': MaDinhDanh,
        'TenDonVi': TenDonVi,
        'ID_GOITHAU': [None for _ in range(len(MaDinhDanh))], # Append later
        'planNo': planNo,
        'planID': planID,
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
        'TGIAN_BATDAU_TOCHUC_LCNT_CHITIET': [convert_date_get_to_final_date(val) if val else None for val in TGIAN_BATDAU_TOCHUC_LCNT],
        'MA_TBMT': MA_TBMT,
        'ID_TBMT': ID_TBMT,

        'STATUS_TBMT': STATUS_TBMT,
        "STATUS_BID": STATUS_BID,
        
        "MAPPING_STATUS_TBMT": [MAPPING_STATUS_TBMT(STT_TBMT=val_1, HINHTHUC_LCNT=val_2) for val_1, val_2 in zip(STATUS_TBMT, HINHTHUC_LCNT)],
        
        "linkNotifyInfo": linkNotifyInfo,
        "numBidderJoin": numBidderJoin,
        "bidRealityOpenDate": bidRealityOpenDate,
        "PHANLOAI_NGUONVON": PHANLOAI_NGUONVON,
        "THAMQUYEN_PHEDUYET": THAMQUYEN_PHEDUYET,
        "ACTION": ACTION
    }

    GOI_THAU = pd.DataFrame(data)
    
    # Update ID_GOI_THAU
    GOI_THAU['ID_GOITHAU'] = get_IdGoiThau(data_base, planNo_now=plan, len_df_now=len(GOI_THAU))
    
    return GOI_THAU