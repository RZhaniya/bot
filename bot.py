# import config
import telebot
from telebot import types
from string import Template
bot = telebot.TeleBot('5492359365:AAEjmoizJFCM5rYoMbtQ5S4KyFn4U0CT4SY')
# bot = telebot.TeleBot(config.token)

user_dict = {}

class User:
    def __init__(self, city):
        self.city = city
        self.fullname = ''
        self.phone = ''
        self.mail = ''
        # keys = ['full name', 'phone', 'mail']
        
        # for key in keys:
        #     self.key = None

# если /help, /start
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/reg')
    itembtn3 = types.KeyboardButton('/reg2')
    markup.add(itembtn1, itembtn2, itembtn3)

    bot.send_message(message.chat.id, "Здравствуйте "
    + message.from_user.first_name
    + ", я бот, чтобы вы хотели узнать?", reply_markup=markup)

# /about
@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, "Мы надежная компания"
    + " company. 10 лет на рынке.")

# /reg
@bot.message_handler(commands=["reg"])
def user_reg(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Казахстан')
    itembtn2 = types.KeyboardButton('Узбекистан')
    itembtn3 = types.KeyboardButton('Кыргызстан')
    itembtn4 = types.KeyboardButton('Таджикистан')
    itembtn5 = types.KeyboardButton('Туркменистан')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)

    msg = bot.send_message(message.chat.id, 'Ваша страна?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_city_step)

def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)
        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, "Фамилия Имя Отчество", reply_markup=markup)
        bot.register_next_step_handler(msg, process_fullname_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!!')

def process_fullname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.fullname = message.text

        msg = bot.send_message(chat_id, "Ваш номер телефона")
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')  


def process_phone_step(message):
    try:
        # int(message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, "Ваша электронная почта")
        bot.register_next_step_handler(msg, process_mail_step)

    except Exception as e:
        bot.reply_to(message, 'ooops!!')  



def process_mail_step(message):
    try:

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.mail = message.text
        
        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(user, 'Ваша заявка', message.from_user.first_name), parse_mod="Markdown")

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"
def getRegData(user, title, name):
    t = Template('$title *$name* \n Город: *$userCity* \n ФИО: *$fullname* \n Телефон: *$phone* \n Ваша почта: *mail* ')

    return t.substitute({
        'title': title,
        'name': name,
        'userCity': user.city,
        'fullname': user.fullname,
        'phone': user.phone,
        'mail': user.mail,
    })

# произвольный текст
@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(message.chat.id, '0 нас - /about\nРегистрация - /reg\nПомощь - /help')

# произвольное фото
@bot.message_handler(content_types=["photo"])
def send_help_text(message):
    bot.send_message(message.chat.id, 'Напишите текст')


bot. enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)


