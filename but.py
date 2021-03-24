import json
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler
import openpyxl
wb = openpyxl.load_workbook('Questions.xlsx')
sheet = wb.active
#for i in range (1, 4) :
{ cell = sheet.cell(row=2,column=2),
print(cell.value)}

TOKEN = "001.3273522775.2055291012:752357883" #your token here

bot = Bot(token=TOKEN)


def buttons_answer_cb(bot, event):
    if event.data['callbackData'] == "call_back_id_2":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Hey! It's a working button 2.",
            show_alert=True
        ) 


    elif event.data['callbackData'] == "dislike":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text=".",
            show_alert=False
        )

    elif event.data['callbackData'] == "call_back_id_4":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Hey! It's a working button 3.",
            show_alert=False
        )

def message_cb(bot, event):
    {bot.send_text(chat_id=event.from_chat,
                text=sheet['A3'].value,
                inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "Ситуацию в мире", "url": "http://mail.ru"},
                      {"text": sheet['B3'].value, "callbackData": "call_back_id_2", "style": "attention"}],
                      [{"text": " 👎 ", "callbackData": "dislike"},
                      {"text": "444", "callbackData": "call_back_id_4", "style": "primary"}
                ]]))),
    bot.send_text(chat_id=event.from_chat, text="блабла")}


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))

bot.start_polling()
bot.idle()