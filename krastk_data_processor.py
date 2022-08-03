import configparser,os
import pandas as pd
import math

from yaml import load
from rabbit import result_to_df,scr_to_df
from openpyxl import load_workbook


config = configparser.ConfigParser()
config.read(os.path.basename(__file__).split('.')[0]+".cfg")

if __name__ == "__main__":
    for key in config.sections():
        worksheet = config[key]['worksheet']
        result = config[key]['result']
        scr = config[key]['scr']
        workbook = config[key]['workbook']
        print(f'writing {worksheet} ...to {workbook} using:\n\tresult:{result}\n\tscr:{scr}')
        # # create dataset 
        df_result = result_to_df(result)
        df_ar=scr_to_df(scr)
        df = pd.merge(df_result, df_ar, on='id')
       
        if os.path.exists(workbook):
            with pd.ExcelWriter(workbook,  mode="a", engine='openpyxl',if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name=worksheet)

        else:
            df.to_excel(workbook, sheet_name = worksheet)
