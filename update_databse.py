import sqlite3
import json
import requests
import time
import re



api_key_fIle = open("영월고등학교 학생회 봇\\secret\\naver_api_key.txt",encoding="utf-8")
api_key = api_key_fIle.read()
api_key_fIle.close()


year_and_month = int(time.strftime('%Y%m', time.localtime(time.time())))
p = re.compile("[^0-9]")

URL = "http://open.neis.go.kr/hub/mealServiceDietInfo?KEY="+ api_key +"&ATPT_OFCDC_SC_CODE=K10&SD_SCHUL_CODE=7800076&MLSV_FROM_YMD="+str(year_and_month)+"&MLSV_TO_YMD"+str(year_and_month+2)+"&Type=json"
response = requests.get(URL) 
data = json.loads(response.text)

updated_database = []

for i in range(len(data["mealServiceDietInfo"][1]["row"])):
    data["mealServiceDietInfo"][1]["row"][i]["DDISH_NM"] = "".join(p.findall(data["mealServiceDietInfo"][1]["row"][i]["DDISH_NM"].replace("<br/>","\n").replace(".","")))
    updated_database.append((None ,data["mealServiceDietInfo"][1]["row"][i]["MLSV_TO_YMD"], data["mealServiceDietInfo"][1]["row"][i]["MMEAL_SC_NM"]  ,data["mealServiceDietInfo"][1]["row"][i]["DDISH_NM"]))


conn = sqlite3.connect("영월고등학교 학생회 봇\\datebase.db") 
cur = conn.cursor()

conn.execute('DROP TABLE IF EXISTS meal_data')
conn.execute('CREATE TABLE IF NOT EXISTS meal_data(id INTEGER PRIMARY KEY, date TEXT, kind TEXT, content TEXT)') 
cur.executemany('INSERT INTO meal_data VALUES (?, ?, ?, ?)', updated_database) 

conn.commit()
conn.close()
