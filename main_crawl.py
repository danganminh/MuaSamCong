import os
import sys
import asyncio
import threading
from datetime import datetime
import pandas as pd

import GoogleSheet_Works
from send_mess import telegram_send
from functions.my_driver import custom_driver
from functions.logic import MAPPING_TENDONVI
from functions.module_1 import module_1
from functions.module_2 import module_2

lock = threading.Lock()

list_of_sheets = ['2.1.KHLCNT', '2.1.GOI_THAU', '2.1.GOI_THAU_CT', '2.1.GIA_HAN', '2.1.LAM_RO',
                  '2.1.KIEN_NGHI', '2.1.BIENBAN_MOTHAU', '2.1.HSDXKT', '2.1.HSDXTC', '2.1.KQLCNT']

time_string = str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))

list_KHLCNT_df = []
list_GOI_THAU_df = []
list_GOI_THAU_CT_df = []
list_GIA_HAN_df = []
list_LAM_RO_df = []
list_KIEN_NGHI_df = []
list_BIENBAN_MOTHAU_df = []
list_HSDXKT_df = []
list_HSDXTC_df = []
list_KQLCNT_df = []

all_df = {}
messages = {}

async def send_mess_to_telegram(all_mess):
    if all_mess:
        for mess in all_mess:
            if mess:
                await telegram_send(mess)
                await asyncio.sleep(5)


def append_global_list(df, target_list_df):
    global lock
    with lock:
        target_list_df.append(df)


def add_dict_global(list_, name):
    global lock
    with lock:
        messages[name] = list_
        
        
async def get_module_1(KEY, data_base):
    driver = None
    try:
        driver = custom_driver(headless=False)
        results = module_1(driver, data_base, KEY)
        driver.quit()
        add_dict_global(results[-2], 'KHLCN')
        add_dict_global(results[-1], 'TBMT')
        dataframes = results[:-2]
        for result, target_list in zip(dataframes, [list_KHLCNT_df, list_GOI_THAU_df, list_GOI_THAU_CT_df,
                                                    list_GIA_HAN_df, list_LAM_RO_df, list_KIEN_NGHI_df,
                                                    list_BIENBAN_MOTHAU_df, list_HSDXKT_df, list_HSDXTC_df,
                                                    list_KQLCNT_df]):
            append_global_list(result, target_list)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()


async def get_module_1_multip_threads():
    
    number_driver = 4
    MAPPING_TENDONVI_VAR = MAPPING_TENDONVI()
    MAPPING_TENDONVI_KEY = MAPPING_TENDONVI_VAR.keys()
    total = len(MAPPING_TENDONVI_KEY)
    BATCH_SIZE = total // number_driver
    steps = total // BATCH_SIZE
    if steps * BATCH_SIZE < total:
        steps += 1

    all_keys = []
    for step in range(steps):
        start_idx = step * BATCH_SIZE
        end_idx = (step + 1) * BATCH_SIZE
        batch_indices = list(MAPPING_TENDONVI_KEY)[start_idx:end_idx]
        print(batch_indices)
        all_keys.append(batch_indices)

    data_base = all_df['2.1.KHLCNT']
    threads = []
    for key in all_keys:
        if not key:
            continue
        t = threading.Thread(target=lambda: asyncio.run(get_module_1(key, data_base)))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()

    for sheet, target_list_df in zip(list_of_sheets, [list_KHLCNT_df, list_GOI_THAU_df, list_GOI_THAU_CT_df,
                                                      list_GIA_HAN_df, list_LAM_RO_df, list_KIEN_NGHI_df,
                                                      list_BIENBAN_MOTHAU_df, list_HSDXKT_df, list_HSDXTC_df,
                                                      list_KQLCNT_df]):
        df = pd.concat(target_list_df, ignore_index=True)
        GoogleSheet_Works.append_gsheet(df=df, range_data=sheet)

    # await asyncio.gather(
    #     send_mess_to_telegram(messages['KHLCN']),
    #     send_mess_to_telegram(messages['TBMT'])
    # )


async def get_module_2():
    driver = None
    try:
        driver = custom_driver()
        dict_data, dict_mess = module_2(driver, all_df)
        driver.quit()

        for sheet in list_of_sheets:
            GoogleSheet_Works.update_gsheet(df=dict_data[sheet], range_data=sheet)

        await asyncio.gather(
            send_mess_to_telegram(dict_mess['TBMT']),
            send_mess_to_telegram(dict_mess['GIA_HAN']),
            send_mess_to_telegram(dict_mess['LAM_RO']),
            send_mess_to_telegram(dict_mess['KIEN_NGHI']),
            send_mess_to_telegram(dict_mess['HUY_THAU']),
            send_mess_to_telegram(dict_mess['OPENED_BID_1_MTHS']),
            send_mess_to_telegram(dict_mess['OPENED_DXKT']),
            send_mess_to_telegram(dict_mess['PUBLISH']),
            send_mess_to_telegram(dict_mess['APPROVED_DXKT']),
            send_mess_to_telegram(dict_mess['OPENED_DXTC'])
        )

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()


async def main():
    
    path_log = 'log_files'
    if not os.path.exists(path_log):
        os.makedirs(path_log)

    old_stdout = sys.stdout
    name_log = f'log_{time_string}.txt'
    log_file = open(os.path.join(path_log, name_log),"w")
    sys.stdout = log_file
        
    print('Get All data from Google Sheets !!!')
    for sheet in list_of_sheets:
        df_cache = GoogleSheet_Works.get_data(range_data=sheet)
        path_cache = f'{sheet}_cache.csv'
        df_cache.to_csv(path_cache, index=False)
        df = pd.read_csv(path_cache)
        all_df[sheet] = df
        os.remove(path_cache)
        
    # print("\n\n Start Module 1 !!!\n\n")
    # await get_module_1_multip_threads()

    print("\n\n Start Module 2 !!!\n\n")
    await get_module_2()
    
    sys.stdout = old_stdout
    log_file.close()

if __name__ == '__main__':
    asyncio.run(main())
