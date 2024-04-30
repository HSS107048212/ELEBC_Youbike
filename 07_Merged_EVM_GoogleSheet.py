# -*- coding: utf-8 -*-
"""05_AC-PV.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1oozHEqsPf8igOTnOPeqSAk4CU6vhruaB

## Get Excel in the folder
"""

# 讀取資料夾中的excel檔名
import os
import pandas as pd
# 指定你的目錄路徑
directory_path = 'C:/Users/Elebc_GPU_Server/Desktop/排程抓資料/'
# C:/Users/Elebc_GPU_Server/Desktop/排程抓資料/
# /content/


## Get EVM_Excel in the folder
# 獲取目錄中的所有檔案和子目錄名稱
files_and_directories = os.listdir(directory_path)
print(files_and_directories)
file_EVM=[]
for item in files_and_directories:
    # 檢查是否包含指定日期和文件名
    if "EVM" in item:
        print("Matched File:", item)
        file_EVM.append(item)

# 打印出列表
print(file_EVM)

"""## Filter the start day (UI: days)"""

import os
import datetime

# 獲取今天的日期
today = datetime.date.today()

# 計算 ? 天前的日期開始的資料
## 後續會接for迴圈，所以假設days=5，那麼前5天，前4天，前3天，前2天，前1天都會被計算。
## 如果days=1，那麼就是算前1天。
## 如果days=0，那麼就是只計算當天。
days_ago = today - datetime.timedelta(days=0) #後續更改----------------------------------------------------------------------------

# 將日期格式化為 YYYY-MM-DD
formatted_date = days_ago.strftime('%Y-%m-%d')
print(formatted_date)


# 排序文件名列表，假設日期和時間格式固定，可以直接按字符串排序
matched_files_EVM = [f for f in file_EVM if formatted_date <= f ]
matched_files_EVM = sorted(matched_files_EVM)

# 打印出匹配的文件名
print("EVM files are:", matched_files_EVM)

"""## Processing Function: Compute AC (UI: Rides_day_for_breakeven)"""

import numpy as np
"""## Import EV_AC_PV file to Google drive"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 設置Google Drive API的認證
credentials = service_account.Credentials.from_service_account_file(
    f'{directory_path}rich-operand-418201-63c868c738c8.json',  # 請替換成你的認證文件路徑
    scopes=['https://www.googleapis.com/auth/drive']
)

# 創建Google Drive API的服務
drive_service = build('drive', 'v3', credentials=credentials)
# 要上傳到的Google Drive文件夾的ID
folder_id = '1aeTv-6l0nfmpEAfKHBvd7l5p0l9Kfplb'  # 請替換成目標文件夾的ID

"""## Main Function: Input Youbike 2.0 Data to Processing Function"""

files_EVM = [(f"{directory_path}{filename}", filename[0:10]) for filename in matched_files_EVM]
print(files_EVM)
print()

## 如何整併每一天的資料，進去以往的累積的資料？
## 0. 開啟Google sheet API
## 1. 開設一個Google sheet，儲存「累積至前天」的資料
## 2. 讀取「累積至前天」的資料 from Google sheet
## 3. 將「累積至前天」與「昨天」的資料進行合併
## 4. 將合併好的資料重新上傳到Google sheet


### 以下還沒有決定好該怎麼做！！！
for file_path, time_label in files_EVM:
            # 使用左表格的sns列與右表格的ID列進行left join，合併成EV_AC_PV的檔案

            AC_PV_data = pd.read_excel(file_path)

            # 要上傳的Excel文件路徑
            excel_file_path = f'{directory_path}{time_label} EVM.xlsx'  # 請替換成你的Excel文件路徑
            import os
            
            # 上傳文件
            file_metadata = {
                'name': os.path.basename(excel_file_path),
                'parents': [folder_id]
            }
            media = MediaFileUpload(excel_file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

            print('File ID: %s' % file.get('id'))