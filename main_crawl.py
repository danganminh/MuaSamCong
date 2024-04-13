import pandas as pd
from datetime import date

from functions.logic import MAPPING_TENDONVI
from functions.module_1 import module_1
from functions.custom_driver import custom_driver

if __name__ == '__main__':
    
    data_base = pd.ExcelFile('DATA-BanQLDT.xlsx')
    driver = custom_driver()    
    
    df, df_2, df_3, df_4, df_5, df_6, df_7, df_8, df_9, df_10 = module_1(driver, data_base, MAPPING_TENDONVI())
    df.to_excel('GOI_THAU.xlsx', index=False)
    df_2.to_excel('GOI_THAU_CT.xlsx', index=False)
    df_3.to_excel('KHLCNT.xlsx', index=False)
    df_4.to_excel('LAM_RO.xlsx', index=False)
    df_5.to_excel('KIEN_NGHI.xlsx', index=False)
    df_6.to_excel('GIA_HAN.xlsx', index=False)
    df_7.to_excel('BIENBAM_MOTHAU.xlsx', index=False)
    df_8.to_excel('HSDHKT.xlsx', index=False)
    df_9.to_excel('HSDXTC.xlsx', index=False)
    df_10.to_excel('Kqua.xlsx', index=False)


    driver.quit()
    data_base.close()

    