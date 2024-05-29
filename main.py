import config
import telebot
from telebot import types
import time


class User:
    def __init__(self):
        self.last_t = 0
        self.limit = 0

users = {}
bot = telebot.TeleBot(config.token)

@bot.message_handler(content_types=['text', 'audio', 'document', 'photo', 'sticker', 'video', 'video_note', 'voice', 'location', 'contact'])
def on_message(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "проверОчка бота")
    else:
        if message.chat.id != config.target_chat:
            is_photo = message.content_type in ('photo', 'video', 'audio', 'document', 'voice')
            if message.chat.id not in users: users[message.chat.id] = User()
            if (time.time() - users[message.chat.id].last_t) >= config.timeout:
                users[message.chat.id].limit = 10 if is_photo else 0
                forward(message)
            elif (is_photo and users[message.chat.id].limit > 0):
                users[message.chat.id].limit -= 1
                forward(message, users[message.chat.id].limit)
            else:
                print(f'W: Сообщение до таймаута от tg://user?id={message.chat.id}')
                users[message.chat.id].limit = 0
                bot.send_message(message.chat.id, 'Превышен лимит сообщений. Ещё терпеть: {0:.1f}сек'.format(
                    config.timeout + users[message.chat.id].last_t - time.time()
                ))

def forward(message, limit = None):
    users[message.chat.id].last_t = time.time()
    bot.forward_message(config.target_chat, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, f'Отправлено: {11 - limit}. Максимум 10 за раз.' if limit else "Спасибки")

print("Running...")
bot.infinity_polling()
