import telebot
from telebot import types
import schedule
import threading
import time
import params

TOKEN = params.TOKEN
bot = telebot.TeleBot(TOKEN)

import dataBase
import db_connect


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('Текущие заказы')
    markup.add(item1)
    dataBase.db_connect(message.chat.id)
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!\n С моей помощью ты сможешь отслеживать онлайн заказы от Алисы! Начнем'.format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Текущие заказы':
            name = dataBase.db_orders_name(message.chat.id)
            orders = dataBase.db_not_done(name[0][0])
            if(len(orders)==0):
                bot.send_message(message.chat.id,"Все заказы выполнены")
            else:
                message_order(orders)

def newOrder():
    message_order(dataBase.db_orders())


def message_order(orders):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Заказ готов', callback_data='delete'))

    order = ""
    for mes in orders:
        order += "Заказ №: " + str(mes[3])
        order += "\nПозиции:\n"
        print(mes)
        order += mes[1]
        order += "\n\nАдрес: " + mes[2]
        dataBase.db_orders_read(mes[3])
        id = dataBase.db_orders_id(mes[0])
        print(id)
        nDone_order = bot.send_message(id[0][0], order, reply_markup=markup)
        dataBase.db_order_mes_id(nDone_order.message_id, mes[3])
        order = ''


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.message:
         if callback.data == 'delete':
            dataBase.db_done(callback.message.message_id)
            bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=callback.message.message_id,
                text="Отправлен")



def runDataBase():
    db_connect.main()
    newOrder()

schedule.every(20).seconds.do(runDataBase)

while True:
    schedule.run_pending()
    time.sleep(1)
def runBot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    t1 = threading.Thread(target=runBot)
    t3 = threading.Thread(target=runDataBase)
    t1.start()
    t1.join()  # wait for t1 to complete for up to 10 seconds
    t3.start()
    t3.join()









