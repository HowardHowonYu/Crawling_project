# -*- coding: utf-8 -*-

import json
from slacker import Slacker
from flask import Flask, request, make_response
import sys

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker #sql에 연결 시켜주는 함수
import pandas as pd

import MySQLdb.cursors
key = "data"



# engine = create_engine("mysql://root:dss@15.164.136.109/job_hunter?charset=utf8mb4")
# QUERY = "SELECT * FROM job_hunter WHERE position '{}';".format("data")
# city_df = pd.read_sql(QUERY,engine)


token  = "xoxb-881894006755-1009615633511-bTqIzFjWZ1hdQTL9h6n06FXu"
slack = Slacker(token)



app = Flask(__name__)
@app.route("/help", methods=["GET", "POST"])
def help_msg():
    return "'@Job Hunter' 를 입력하시고 검색하고 싶으신 '키워드' 를 입력하세요."


@app.route("/slack", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)
    # print("="*100) 
    # print(slack_event)
    
    # 1이 입력 없음, 2가 입력 있음
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})
        
    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)

    
    # return make_response("슬랙 요청에 이벤트가 없습니다.", 404, {"X-Slack-No-Retry": 1})


def get_answer(result):   
    attachments = []
    for i in range(0,len(result)):
        attachments_dict = dict()
        attachments_dict['title'] = "# " + result[i][4] 
        attachments_dict['title_link'] = result[i][5]
        attachments_dict['text'] = result[i][2] + " : " + result[i][3][:30] + " \n " + result[i][7]
        # attachments_dict['mrkdwn_in'] = ["title" ,"text", "pretext"]  # 마크다운을 적용시킬 인자들을 선택합니다.    
        attachments.append(attachments_dict)

    return attachments



# 이벤트 핸들하는 함수

def event_handler(event_type, slack_event):
    error_attachments_dict = dict()
    error_attachments_dict['title'] = "키워드를 입력하세요"
    error_attachments_dict['text'] = "예)  '데이터' , 'data Science' 등"
    error_attachments = [error_attachments_dict]

    def send_data():
        channel = slack_event["event"]["channel"]
        user_input = slack_event['event']['blocks'][0]['elements'][0]['elements']
        if len(user_input) >= 2:
            keyword = user_input[1]['text']
            con = MySQLdb.connect(user='root', passwd='dss', db='job_hunter', host='15.164.136.109', charset="utf8", use_unicode=True)
            cursor = con.cursor()
            sql = "SELECT * FROM job_hunter WHERE position like '%{}%' order by deadline".format(keyword)
            cursor.execute(sql)
            result = cursor.fetchall()
            attachments = get_answer(result)
            slack.chat.post_message(channel, text="키워드 '{}' 에 관한 검색 결과 입니다.".format(keyword), attachments=attachments, as_user=True)
            # event_type = None
            return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )
        else:      
            slack.chat.post_message(channel, text=None, attachments=error_attachments ,as_user=True)

    if event_type == "app_mention":
        send_data()
            # event_type = None
    # elif event_type == 'message':
    #     send_data()
       
    message = "[%s] 이벤트 핸들러를 찾을 수 없습니다." % event_type
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':

    app.run(debug=True)



