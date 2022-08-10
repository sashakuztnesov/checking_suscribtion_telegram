import telebot
import sqlite3 as sql


#База Данных
con = sql.connect("data.db", check_same_thread=False)
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(id INT)")

#Ваш бот
token = ""
bot = telebot.TeleBot(token)

#ID Вашего канала
chan_id = https://t.me/GalaRazhisByb

#Клавиатура для проверки подписки
keyboard = telebot.types.InlineKeyboardMarkup()
subscribe = telebot.types.InlineKeyboardButton(text="Подписаться", url="ссылка на ваш канал")
check = telebot.types.InlineKeyboardButton(text="Проверить", callback_data="check")
keyboard.add(subscribe)
keyboard.add(check)

#Не нужная хуйня, вписал просто для видимости
menu = telebot.types.ReplyKeyboardMarkup(True, True)
menu.add("Вы уже подписаны")


@bot.message_handler(commands=["start"])
def start(message):
    users = cur.execute("SELECT id FROM users WHERE id = ?", (message.chat.id, )).fetchone()
    con.commit()
    if users == None: #Если юзер ещё не в БД
        bot.send_message(message.chat.id, "Что-бы продолжить подпишитесь на канал", reply_markup=keyboard)
    else: #Уже в бд
        bot.send_message(message.chat.id, "Вы уже подписаны", reply_markup=menu)


#Тут мы чекаем подписку
@bot.callback_query_handler(func=lambda call: True)
def c_listener(call):
    if call.data == "check":
        x = bot.get_chat_member(chan_id, call.message.chat.id)

        if x.status == "member" or x.status == "creator" or x.status == "administrator":
            bot.send_message(call.message.chat.id, "Добро пожаловать!", reply_markup=menu)
            cur.execute("INSERT INTO users VALUES(?)", (call.message.chat.id, ))
            con.commit()
        else:
            bot.send_message(call.message.chat.id, "Вы не подписались!", reply_markup=keyboard)



if __name__ == "__main__":
    bot.polling()
