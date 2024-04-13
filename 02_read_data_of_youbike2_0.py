import requests

def fetch_youbike_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data. Status code:", response.status_code)
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

if __name__ == "__main__":
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    youbike_data = fetch_youbike_data(url)
    if youbike_data:
        print("YouBike data retrieved successfully!")
        # 在这里对您的YouBike数据进行处理
    else:
        print("Failed to fetch YouBike data.")

import pandas as pd

# Convert JSON data to DataFrame
df = pd.DataFrame(youbike_data)

df

df.shape

#df = df[["sna","tot","sarea","lat","lng"]]

df["sarea"].unique()

# 将 '臺大公館校區' 替换为 '大安區'
df['sarea'] = df['sarea'].replace('臺大公館校區', '大安區')
df["sarea"].unique()

from datetime import datetime

current_time = datetime.now()
formatted_time = current_time.strftime("%Y-%m-%d %H%M")
print("Current system time (YYYY-MM-DD HHMM):", formatted_time)

df.to_excel(f"{formatted_time}_Youbike_cleaned.xlsx", index=False)

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 設置Google Drive API的認證
credentials = service_account.Credentials.from_service_account_file(
    'C:/Users/Elebc_GPU_Server/Desktop/排程抓資料/rich-operand-418201-63c868c738c8.json',  # 請替換成你的認證文件路徑
    scopes=['https://www.googleapis.com/auth/drive']
)

# 創建Google Drive API的服務
drive_service = build('drive', 'v3', credentials=credentials)

# 要上傳的Excel文件路徑
excel_file_path = f'C:/Users/Elebc_GPU_Server/Desktop/排程抓資料/{formatted_time}_Youbike_cleaned.xlsx'  # 請替換成你的Excel文件路徑

# 要上傳到的Google Drive文件夾的ID
folder_id = '1KPUVieyFuW7vTJ_E4V_fk4O5BGJj1Alm'  # 請替換成目標文件夾的ID

import os

# 上傳文件
file_metadata = {
    'name': os.path.basename(excel_file_path),
    'parents': [folder_id]
}
media = MediaFileUpload(excel_file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

print('File ID: %s' % file.get('id'))