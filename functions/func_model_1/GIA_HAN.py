import pandas as pd
from io import StringIO


def processing_GIA_HAN(driver, data_base, index):

    columns = ['STT', 'Thời điểm gia hạn thành công', 'Thời điểm đóng thầu cũ', 'Thời điểm đóng thầu sau gia hạn', 'Thời điểm mở thầu cũ', 'Thời điểm mở thầu sau gia hạn', 'Lý do']
    df = pd.DataFrame(columns=columns)
    data = []

    # Find table
    all_table = pd.read_html(StringIO(driver.page_source))
    for table in all_table:
        try:
            if len(table.columns) == len(columns) and all(table.columns == columns):
                data = table.values.tolist()
                break
        except:
            continue

    if not data:
        print('None Gia_Han')

    for i in range(len(data)):
        df.loc[i] = data[i]

    rename_list = {
        'MA_TBMT': [data_base['MA_TBMT'].values[index] for _ in range(len(df))],
        'ID_GIAHAN': [None for _ in range(len(df))],
        'LAN_GIAHAN': df['STT'].values,
        'THOIDIEM_MOTHAU_CU': [val if val else None for val in df['Thời điểm mở thầu cũ'].values],
        'THOIDIEM_DONGTHAU_CU': [val if val else None for val in df['Thời điểm đóng thầu cũ'].values],
        'THOIDIEM_MOTHAU_MOI': [val if val else None for val in df['Thời điểm mở thầu sau gia hạn'].values],
        'THOIDIEM_DONGTHAU_MOI': [val if val else None for val in df['Thời điểm đóng thầu sau gia hạn'].values],
        'LYDO': df['Lý do'].values,
        'NGAY_GIAHAN': [val if val else None for val in df['Thời điểm gia hạn thành công'].values],
        'TAIKHOAN_GIAHAN': [None for _ in range(len(df))]
    }

    GIA_HAN_DF = pd.DataFrame(rename_list)
    
    return GIA_HAN_DF