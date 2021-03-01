from flask import Flask, request, jsonify
import json
import datetime
from enum import Enum
import sqlite3


app = Flask(__name__)



class Discrimination(Enum):
    Today_Meal = 1
    Tomorrow_Meal = 2
    Selected_Date = 3


def Meal(discrimination, date):

    try:

        conn = sqlite3.connect("C:\\Users\\yju08\OneDrive\\동기화폴더\\서버용폴더\\영월고등학교 학생회 봇\\datebase.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM meal_data WHERE meal_data.date = {}".format(date))

        breakfast = "해당하는 급식이 없습니다"
        lunch = "해당하는 급식이 없습니다"
        dinner = "해당하는 급식이 없습니다"

        for data in cur.fetchall():
            if data[2] == "조식":
                breakfast = data[3]
            elif data[2] == "중식":
                lunch = data[3]
            elif data[2] == "석식":
                dinner = data[3]

        month = date[4:6]
        day = date[6:]

        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "{}월 {}일 [조식]".format(month,day)+"\n"+breakfast+"\n\n"+ "{}월 {}일 [중식]".format(month,day)+"\n"+lunch+"\n\n"+"{}월 {}일 [석식]".format(month,day)+"\n"+dinner
                        }
                    }
                ],
                "quickReplies": [
                    {
                        "label":"홈으로",
                        "action":"block",
                        "blockId" : "5ea7fc9c8b6993000177b6fe",

                    },
                ]
            }
        }

        if discrimination == Discrimination.Today_Meal:
            res["template"]["quickReplies"].append({"label":"내일급식은?", "action":"block", "blockId" : "5ea7ff16cdbc3a00015a1c7d",})
            res["template"]["quickReplies"].append({"label": "날짜선택","action":"block","blockId" : "5ea7ff204ab83b0001681c89",})

        elif discrimination==Discrimination.Tomorrow_Meal:
            res["template"]["quickReplies"].append({"label":"오늘급식은?", "action":"block", "blockId" : "5ea7cb4a73e9c100015b01dd",})
            res["template"]["quickReplies"].append({"label": "날짜선택","action":"block","blockId" : "5ea7ff204ab83b0001681c89",})

        elif discrimination==Discrimination.Selected_Date:
            res["template"]["quickReplies"].append({"label":"오늘급식은?", "action":"block", "blockId" : "5ea7cb4a73e9c100015b01dd",})
            res["template"]["quickReplies"].append({"label":"내일급식은?", "action":"block", "blockId" : "5ea7ff16cdbc3a00015a1c7d",})
            res["template"]["quickReplies"].append({"label": "날짜선택","action":"block","blockId" : "5ea7ff204ab83b0001681c89",})

        
        


    except Exception as e:

        res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": "버그가 발생했습니다.\n개발자님께 버그를 제보할게요"
                    }
                }
            ],
            "quickReplies": [
                {
                    "label":"홈으로",
                    "action":"block",
                    "blockId" : "5ea7fc9c8b6993000177b6fe",

                    },
                ]
            }
        }
   
        print("\n\n예외가 발생했습니다 : {}".format(e))
        

    finally:
        conn.close()
        return res



@app.route('/TodayMeal', methods=['POST'])
def TodayMeal():

    now = datetime.datetime.now()
    
    return jsonify(Meal(Discrimination.Today_Meal, now.strftime('%Y%m%d')))


@app.route('/TomorrowMeal', methods=['POST'])
def TomorrowMeal():

    today = datetime.datetime.today()
    tomorrow = today + datetime.timedelta( days=1)

    return jsonify(Meal(Discrimination.Tomorrow_Meal, tomorrow.strftime("%Y%m%d")))


@app.route('/SelectDate', methods=['POST'])
def SelectDate():
    req = request.get_json()
    date = json.loads(req["action"]["detailParams"]["date"]["value"])["value"]

    return jsonify(Meal(Discrimination.Selected_Date, date.replace("-","")))




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, threaded=True)
