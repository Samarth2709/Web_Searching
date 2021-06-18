import pandas as pd
import ask_google
import numpy as np
import time

start_time = time.time()
filename = "Python Pull.xlsx"
sheetname = None

if sheetname != None:
    df = pd.read_excel(filename, sheet_name=sheetname)
else:
    df = pd.read_excel(filename)

search_col = "Group Name"

search_col_data = df[search_col]
output_list = []
set = 0
print(len(search_col_data))
for i, element in enumerate(list(search_col_data)):
    print(i)
    print(element)
    set +=1
    if set == 50:
        print("SLEEP")
        time.sleep(45)
        print("AWAKE")
        set = 0
    output_list.append(ask_google.ask_google(str(element) + " founded?"))
    print(output_list[-1])
    time.sleep(2.5)

    if set%20 == 0:
        good_none = False
        for output in output_list[i-15:]:
            if output!= None:
                good_none = True
                break
        if good_none == False:
            print(False)


output_col_name = "OUTPUT"
df[output_col_name] = pd.Series(np.array(output_list))

df.to_excel(filename[:-5]+'(OUTPUT).xlsx', index=False)
print("SAVED")
print(time.time()-start_time)