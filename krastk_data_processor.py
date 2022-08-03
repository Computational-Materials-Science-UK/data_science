import configparser,os
import pandas as pd
import math

from yaml import load
from rabbit import result_to_df,scr_to_df
from openpyxl import load_workbook
from openpyxl.chart import (
    ScatterChart,LineChart,
    Reference,
    Series,
)

config = configparser.ConfigParser()
config.read(os.path.basename(__file__).split('.')[0]+".cfg")

# def create_chart(sheet,df):
#     refObj = Reference(sheet, min_col=1, min_row=1, max_col=1,max_row=10)
#     seriesObj = Series(refObj, title='First series')


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
        df_rows = len(df.index)

        if os.path.exists(workbook):
            with pd.ExcelWriter(workbook,  mode="a", engine='openpyxl',if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name=worksheet)

        else:
            df.to_excel(workbook, sheet_name = worksheet)

def create_charts():                
    wb=writer.book
    ws = writer.sheets[worksheet]
    ws.title=worksheet
    chart = LineChart()  # first y axis
    chart.style = 13
    
    x = Reference(ws, min_col= 3, min_row=2,  max_row = 20)
    y = Reference(ws, min_col= 19, min_row=2,  max_row = 20)
    series = Series(  y,xvalues=x)
    
    print(x)
    print(y)
    chart.series.append(series)

    # chart.x_axis.scaling.min = 0
    # chart.y_axis.scaling.min = 0
    # chart.x_axis.scaling.max = 40
    # chart.y_axis.scaling.max = 0.1

    # chart.add_data(y_values, titles_from_data = True)
    # chart.set_categories(x_values)
    # chart.width = 20
    # chart.height = 10

    # chart.title = 'Fruit Sale'
    # chart.x_axis.title = 'Month'
    # chart.y_axis.title = 'Fruit Sales (USD Mil)'
    chart.legend.position = 'b'
    ws.add_chart(chart, 'A40')
    wb.save(workbook)
print('done running.')