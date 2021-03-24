import json
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
import pandas as pd
import numpy as np
import time


Data_1 = pd.read_excel('Questions 2.xlsx')

Que = Data_1['Questions']
ans1 = Data_1['Ans_1']
ans2 = Data_1['Ans_2']
ans3 = Data_1['Ans_3']

Que = Data_1['Questions']
ans1 = Data_1['Ans_1']
ans2 = Data_1['Ans_2']
ans3 = Data_1['Ans_3']
for i in range(len(Data_1.iloc[1])):
    for j in range(len(Data_1['Ans_1'])):
       Data_1.iloc[j,i] = str(Data_1.iloc[j,i])

id_user = []
que_user = []
ans_user = []

# def quize(event.from_chat):


TOKEN = "001.3273522775.2055291012:752357883" #your token here

bot = Bot(token=TOKEN)

def buttons_answer_cb(bot, event):
    if event.data['callbackData'] == "call_back_id_1":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text=Data_1.iloc[0,1],
            show_alert=False
        )
        


    elif event.data['callbackData'] == "call_back_id_2":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text=Data_1.iloc[0,2],
            show_alert=False
        )
        

    elif event.data['callbackData'] == "call_back_id_3":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text=Data_1.iloc[0,3],
            show_alert=False
        )
        



def message_cb(bot, event):
    bot.send_text(chat_id=event.from_chat,
                text=Que[0],
                inline_keyboard_markup="{}".format(json.dumps([[
                    {"text": Data_1.iloc[0,1], "callbackData": "call_back_id_1", "style": "primary"},
                    {"text": Data_1.iloc[0,2], "callbackData": "call_back_id_2", "style": "primary"},
                    {"text": Data_1.iloc[0,3], "callbackData": "call_back_id_3", "style": "primary"}
                ]])))





bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))

time.sleep(5)

bot.start_polling()
bot.idle()