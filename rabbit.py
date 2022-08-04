import pandas as pd
import numpy as np
import pprint,re,math,os
from statistics import mean 
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score,recall_score,precision_score,f1_score,confusion_matrix,roc_auc_score, r2_score
import openpyxl

def model_evaluation(model_name,Y_test,Y_pred):
    try:
        acc=round(accuracy_score(Y_test,Y_pred)*100,2)
        precision=round(precision_score(Y_test,Y_pred) *100,2)
        recall=round(recall_score(Y_test,Y_pred) *100,2)
        f1=round(f1_score(Y_test,Y_pred) *100,2)
    except:
        acc="-"
        precision="-" 
        recall="-"
        f1="-"
    auc_score=round(roc_auc_score(Y_test,Y_pred)*100,2)
    
    
    
    evaluation={'accuracy': acc,
               'recall': recall,
               'precision': precision,
               'F1 score': f1,
               'auc score': auc_score,              
                }
    df_eval = pd.DataFrame.from_dict(evaluation,orient='index',columns=[model_name])
    return df_eval

def find_outliers(df, col_name):
    Q1 = df[col_name].quantile(0.25)
    Q3 = df[col_name].quantile(0.75)
    IQR = Q3-Q1
    low  = Q1-1.5*IQR
    high = Q3+1.5*IQR
    
    outlier_list=((df[col_name] < low) | (df[col_name] > high)).tolist()
    i_outlier=[i for i, x in enumerate(outlier_list) if x]
    return i_outlier 


def feature_plot(df,col_x,col_y):
    plt.rcParams['figure.figsize'] = [12, 8]
    fig, axs = plt.subplots()
    
    axs.scatter(df[col_x],df[col_y])
    axs.set_xlabel(col_x)
    axs.set_ylabel(col_y)
    axs.title.set_text(col_y+' vs '+col_x)
    axs.set_xticks(np.array(df[col_x])[0::5])
    axs.set_xticklabels(np.array(df[col_x])[0::5],rotation=45)
    plt.rcParams['figure.figsize'] = [8, 8]
    plt.yticks(np.array(df[col_y])[0::5])
    plt.show()

def result_to_dict(result_file_path=None):
    '''
    scrape the output.txt file to tabulate the data into a python dictionary.
    '''
    print(f'working on {result_file_path} for results.')
    data=dict()
    with open(result_file_path,'r') as fh:
        lines =fh.readlines() 

    class_rho_ar=None
    
    for line in lines:
        
        if line.startswith('/'):
            
            stl_name=line.split('/')[-1].strip().split('.')[0].strip()
            stl_class_no = re.findall('(\D+)(\d+)',stl_name)
            #Following ids are generated as a serial number 
            # so that the data is in sorted order
            # if we do not convert to int it will be sorted like 1,10,11,12,13,14,15,16,17,18,19,2,20,21
            id = int(stl_class_no[0][1])
            if not class_rho_ar:
                class_rho_ar=stl_class_no[0][0]
            data[id]=dict()
            data[id]['stl_name']=stl_name
            data[id]['id']=id
                    
        else:
            key,value=line.split("=")
            key=key.strip()
            data[id][key]=value.strip()
    # pprint.pprint(data)
    return data

def scr_to_dict(scr_file_path=None):
    data=dict()
    '''
    Scrape the scr file to create dictionary 
    '''
    print(f'working on {scr_file_path} for aspect ratio.')
    armat = []                                                                     # list for storing the cone lengths
    multiarmat = []                                                                # list to store mean of AR for each mRVE

    with open(scr_file_path, "r") as ipfile:                                      # opens the file, creates the file if nonexisting 
        lines=ipfile.readlines()                                                      # reads all the lines of the file
        endrve = '_export'                                                            # string to detect end of each RVE
        searchcone = '_cone' 

                                                                # cone string to be detected
        for i, line in enumerate(lines):                                              # for loop on all the lines in the input file
            if searchcone in line:                                                       # search for cones
                words = re.split(",|\s+", line)                                             # splits the lines usign whitespace, comma and other delimiters
                coneLength = math.sqrt((float(words[1])-float(words[8]))**2+
                                        (float(words[2])-float(words[9]))**2+
                                        (float(words[3])-float(words[10]))**2)               # calculate length of the cone
                radius1 = float(words[4])                                                   # radius 1 of cone 
                radius2 = float(words[6])                                                   # radius 2 of cone
                aspectratio = coneLength/(radius1+radius2)                                  # aspect ratio
                armat.append(aspectratio)                                                   # adds cones length to the list while reading the lines
                armean = mean(armat)                                                        # mean of AR for an RVE
            elif endrve in line: 
                stl_name=line.split('/')[-1].strip().split('.')[0].strip()
                stl_class_no = re.findall('(\D+)(\d+)',stl_name)
                ar_id = int(stl_class_no[0][1])
                data[ar_id]=dict()
                data[ar_id]['stl_name']=stl_name
                data[ar_id]['AR']=armean
                data[ar_id]['id']=ar_id
                multiarmat.append(armean)
                armat = []                                         # reinitializes armat to size zero for a new RVE  
    ipfile.close() 
    # pprint.pprint(data)
    return data                                                      

def result_to_df(result_file_path):  
    return pd.DataFrame.from_dict(result_to_dict(result_file_path),orient='index')

def scr_to_df(scr_file_path):  
    return pd.DataFrame.from_dict(scr_to_dict(scr_file_path),orient='index')  



def process_data_to_spreadsheet(config):
    set_workbook=set()
    
    
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
            
        set_workbook.add(workbook)
    for book in set_workbook:

        if os.path.exists(book):print('spreadsheet Created')          
def merge_worksheet_data(workbook):
    print(f'Creating plots on {workbook}')
    df_map = pd.read_excel(workbook,engine='openpyxl',sheet_name=None)
    df = pd.concat(df_map, ignore_index=True)
    with pd.ExcelWriter(workbook,  mode="a", engine='openpyxl',if_sheet_exists="replace") as writer:
                df.to_excel(writer, sheet_name="all_data")
                
def generate_plots(workbook):
    
    print(f'Creating plots on {workbook}')
    df_map = pd.read_excel(workbook,engine='openpyxl',sheet_name=None)
    # df=df_map['highrho-lowar']
    for key in df_map:
        df=df_map[key]
        i=50
        target_param=['AR','C11','Mesh volume']

        for col_x in target_param:
            y = df['E1']
            x = df[col_x]
            


            fig, ax = plt.subplots()
            ax.set(title = f'E1 vs {col_x}',
                xlabel = col_x,
                ylabel = 'E1')

            ax.yaxis.grid()
            ax.xaxis.grid()

            plt.scatter(x, y)
            plt.savefig(f'E1_vs_{col_x}.png')
            wb = openpyxl.load_workbook(workbook)
            ws = wb[key]
            img = openpyxl.drawing.image.Image(f'E1_vs_{col_x}.png')
            img.anchor = f'A{i}'
            i+=25
            ws.add_image(img)
            wb.save(workbook)
    wb.close()

    print('done plotting.') 
