import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression,LogisticRegression
from sklearn.tree import DecisionTreeRegressor

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


def feature_plot(col_x,col_y):
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



   