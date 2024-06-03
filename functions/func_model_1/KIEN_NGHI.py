import pandas as pd
from io import StringIO


def processing_Kien_Nghi(driver, TBMT):

    print(f'Processing Kien_Nghi {TBMT}')

    reqContent = []
    resContent = []
    reqFileName = []
    resFileName = []
    TEN_KIENNGHI = []
    MA_TBMT = []
    ID_TBMT = []

    NGAY_KIENNGHI = []
    MA_DINHDANH_NHATHAU_KIENNGHI = []
    NHATHAU_KIENNGHI = []
    STATUS = []
    resFileId = []
    ID_KIENNGHI = []
    MA_KIENNGHI = []
    reqFileId = []
    reqDate = []
    resDate = []
    petitionPeriod = []
    isDecision = []
    reason = []

    columns = ['STT', 'Loại kiến nghị', 'Tên kiến nghị', 'Nội dung kiến nghị']
    df_temp = pd.DataFrame(columns=columns)
    index = 0    
    
    all_table = pd.read_html(StringIO(driver.page_source))
    for table in all_table:
        try:
            if len(table.columns) == len(columns) and all(table.columns == columns):
                df_temp.loc[index] = table.values[0]
                index += 1
                break
        except:
            continue
    
    reqContent_val = []
    resContent_val = []
    reqFileName_val = []
    resFileName_val = []
    tenkiennghi_val = []
    
    for i, noidung in enumerate(df_temp['Nội dung kiến nghị'].values):
        
        if len(reqContent_val) == len(df_temp): break
        
        if 'Nội dung kiến nghị' in noidung:
            reqContent_val.append(noidung.split('Nội dung kiến nghị  :')[1].split('\n')[0].strip())
        else:
            reqContent_val.append(None)
        if 'Nội dung trả lời' in noidung:
            resContent_val.append(noidung.split('Nội dung trả lời  :')[1].split('\n')[0].strip())
        else:
            resContent_val.append(None)
        if 'File đính kèm nội dung kiến nghị' in noidung:
            reqFileName_val.append(noidung.split('File đính kèm nội dung kiến nghị  :')[1].split('\n')[0].strip())
        else:
            reqFileName_val.append(None)
        if 'File đính kèm nội dung trả lời' in noidung:
            resFileName_val.append(noidung.split('File đính kèm nội dung trả lời  :')[1].split('\n')[0].strip())
        else:
            resFileName_val.append(None)
        
        tenkiennghi_val.append(df_temp['Tên kiến nghị'].iloc[i])
    
    reqContent.extend(reqContent_val)
    resContent.extend(resContent_val)
    reqFileName.extend(reqFileName_val)
    resFileName.extend(resFileName_val)
    TEN_KIENNGHI.extend(tenkiennghi_val)

    for _ in range(len(reqContent)):
        MA_TBMT.append(TBMT)
        ID_TBMT.append(driver.current_url.split('&id=')[1].split('&')[0])

        NGAY_KIENNGHI.append(None)
        MA_DINHDANH_NHATHAU_KIENNGHI.append(None)
        NHATHAU_KIENNGHI.append(None)
        STATUS.append(None)
        resFileId.append(None)
        ID_KIENNGHI.append(None)
        MA_KIENNGHI.append(None)
        reqFileId.append(None)
        reqDate.append(None)
        resDate.append(None)
        petitionPeriod.append(None)
        isDecision.append(None)
        reason.append(None)


    data = {
        'petitionPeriod': petitionPeriod,
        'isDecision': isDecision,
        'reason': reason,
        'reqContent': reqContent,
        'resContent': resContent,
        'reqDate': [val if val else None for val in reqDate],
        'resDate': [val if val else None for val in resDate],
        'reqFileName': reqFileName,
        'reqFileId': reqFileId,
        'resFileName': resFileName,
        'resFileId': resFileId,
        'ID_KIENNGHI': ID_KIENNGHI,
        'MA_KIENNGHI': MA_KIENNGHI,
        'TEN_KIENNGHI': TEN_KIENNGHI,
        'NGAY_KIENNGHI': [val if val else None for val in NGAY_KIENNGHI],
        'MA_DINHDANH_NHATHAU_KIENNGHI': MA_DINHDANH_NHATHAU_KIENNGHI,
        'NHATHAU_KIENNGHI': NHATHAU_KIENNGHI,
        'STATUS': STATUS,
        'MA_TBMT': MA_TBMT,
        'ID_TBMT': ID_TBMT
    }

    KIEN_NGHI = pd.DataFrame(data)
    
    return KIEN_NGHI
