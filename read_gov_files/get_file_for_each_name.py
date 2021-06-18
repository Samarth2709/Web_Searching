import os
import pandas as pd
import glob
import numpy as np
import time


def read_df(filename, sheet_name = "Sheet1"):
    df = pd.read_excel(filename, sheet_name = sheet_name)
    return df


def get_col(df, col_name):
    return list(df[df[col_name].notnull()][col_name])


os.chdir(r'C:\Users\samar\Desktop\Web_Searching\read_gov_files\txt_files_of_gov')

txt_files = glob.glob('*.txt')
print(txt_files)
print("Amount of text files", len(txt_files))

filename = "Python Pull PDF.xlsx"
os.chdir(r'C:\Users\samar\Desktop\Web_Searching\read_gov_files')
df = read_df(filename = filename)
col_links = get_col(df, "SEC (Temp)")
for i in range(5):
    print("CHeck")
print("Column df length: ", len(col_links))
# for link_df in col_links:
#     if "https:/" not in link_df:
#         col_links.remove(link_df)
def revert_original_link(changed_link:str):
    changed_link.replace('&', "/")
    changed_link.replace('!', "?")
    return changed_link

    # original / are &
    # original ? are  !

def format_link(link):
    return link.replace('/', '&').replace('?', '!')[20:-4] + ".txt"
    # original / are &
    # original ? are  !

for df_link in col_links:
    if format_link(df_link) not in txt_files:
        print(df_link)
print("S")
for df_link in col_links:
    if "sec" not in df_link:
        print(df_link)

