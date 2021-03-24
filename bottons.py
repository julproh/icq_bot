
import json
from bot.bot import Bot
from bot.handler import MessageHandler, BotButtonCommandHandler


TOKEN = "001.3273522775.2055291012:752357883" #your token here

bot = Bot(token=TOKEN)

def buttons_answer_cb(bot, event):
    if event.data['callbackData'] == "call_back_id_2":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Hey! It's a working button 2.",
            show_alert=True
        )

    elif event.data['callbackData'] == "call_back_id_3":
        bot.answer_callback_query(
            query_id=event.data['queryId'],
            text="Hey! It's a working button 3.",
            show_alert=False
        )

def message_cb(bot, event):
    bot.send_text(chat_id=event.from_chat,
                  text="Hello with buttons.",
                  inline_keyboard_markup="{}".format(json.dumps([[
                      {"text": "Action 1", "url": "http://mail.ru"},
                      {"text": "Action 2", "callbackData": "call_back_id_2", "style": "attention"},
                      {"text": "Action 3", "callbackData": "call_back_id_2", "style": "primary"}
                  ]])))


bot.dispatcher.add_handler(MessageHandler(callback=message_cb))
bot.dispatcher.add_handler(BotButtonCommandHandler(callback=buttons_answer_cb))

bot.start_polling()
bot.idle()

