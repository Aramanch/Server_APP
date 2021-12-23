import telebot;
import random
bot = telebot.TeleBot('5030941322:AAHFKOho6cfGYh8FwCp0RMhDzagxfPN51Xw');


from telebot import types

login = '';
pin = '';

@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Введите свой логин:");
        bot.register_next_step_handler(message, get_login); #следующий шаг – функция get_login
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg');

def get_login(message): #получаем фамилию
    global login;
    login = message.text;
    bot.send_message(message.from_user.id, 'Введите свой ПИН-код:');
    bot.register_next_step_handler(message, get_pin);

def get_pin(message):
    global pin;
    pin = message.text;


    keyboard = types.InlineKeyboardMarkup(); #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes'); #кнопка «Да»
    keyboard.add(key_yes); #добавляем кнопку в клавиатуру
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no');
    keyboard.add(key_no);
    question = 'Ваш логин '+str(login)+' || Ваш ПИН-код: ' + str(pin) +'?';
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        f = open('user_data.csv', 'r')
        if login == f.readlines()[1] and pin == f.readlines()[3]:
            bot.send_message(call.message.chat.id, 'Пользователь существует');
        else:
            start(bot.send_message(call.message.chat.id, 'Введите повторно /reg'))

        bot.send_message(call.message.chat.id, 'Отправка на сервер...');


    elif call.data == "no":
         start(bot.send_message(call.message.chat.id, 'Введите повторно /reg'))


bot.polling(none_stop=True, interval=0)

