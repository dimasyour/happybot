# -*- coding: utf-8 -*-
import datetime
import logging
import re
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telebot
from telebot import types
from db_worker import *

bot = telebot.TeleBot("1726661536:AAHd5qaDSFLudBdOxoK-Ui_7AUEigFoYoUI")
logging.basicConfig(filename="errors.log", level=logging.INFO)
today = datetime.date.today()
logging.info("Start HappyBot | " + str(today))
PORT = int(os.environ.get('PORT', 80))
TOKEN = '1769553533:AAG6EI51jUJHwAVvYa12iXER7jRniQF_nNM'
helloMessage = '''
Здравствуй {0.first_name}!, рады приветствовать Вас
на сервисе обратной связи
и оценки индекса счастья города Иннополис.
'''

SUZHD_start = []
SUZHD_answer = []

SSSL_start = []
SSSL_answer = []

SUZHD_text = '''
Ниже даны утверждения, с которыми Вы можете согласиться или не согласиться.
Выразите степень Вашего согласия с каждым из них, с помощью эмозди соответствующий оценке:

1. Полностью не согласен 😭
2. Не согласен 😥
3. Скорее не согласен 🥺
4. Нечто среднее 😐
5. Скорее согласен 😌
6. Согласен 😊
7. Полностью согласен 😍
'''

# Вопросы к тесту Динера
SUZHD_question = ['1.В целом моя жизнь близка к идеалу.',
                  '2.Обстоятельства моей жизни исключительно благоприятны.',
                  '3.Я полностью удовлетворен моей жизнью.',
                  '4.У меня есть в жизни то, что мне по-настоящему нужно.',
                  '5.Если бы мне пришлось жить еще раз, я бы оставил все как есть.']
SSSL_text = '''
Для каждого из четырех утверждений выберите, пожалуйста, одну из семи цифр, 
наиболее точно выражающую Ваше ощущение:
Выразите степень Вашего согласия с каждым из них, с помощью эмозди соответствующий оценке:

1. Полностью не согласен 😭
2. 😥
3. 🥺
4. 😐
5. 😌
6. 😊
7. Полностью согласен 😍
'''

# Вопросы к тесту Любомирски
SSSL_question = ['1.В целом я считаю себя счастливым.',
                 '2.По сравнению с большинством сверстников, я более счастлив.',
                 '3.Некоторые люди обычно очень счастливы. Они получают удовольствие от жизни, что бы ни происходило, беря от жизни все. Это похоже на меня.',
                 '4.Когда я просматриваю историю своей жизни, то испытываю удовлетворение от того, как все сложилось.',
                 '5.У меня есть отчетливое чувство, что я живу именно свою жизнь, и что я не поменял(а) бы ее на другую.',
                 '6.Когда я просматриваю историю своей жизни, то испытываю удовлетворение от того, как все сложилось.',
                 '7.Я сумел(а) создать свой собственный дом и образ жизни, которые соответствуют моим предпочтениям.']

# Главное меню
keyboard_Menu = types.InlineKeyboardMarkup()
item_Menu1 = types.InlineKeyboardButton(text='🔎 Оценить уровень счастья', callback_data='grade_menu')
keyboard_Menu.add(item_Menu1)
item_Menu2 = types.InlineKeyboardButton(text='📊 Результаты', callback_data='result_menu')
keyboard_Menu.add(item_Menu2)

# Выбор шкалы оценки
keyboard_test = types.InlineKeyboardMarkup()
item_Test1 = types.InlineKeyboardButton(text='📈 Шкала С.Любомирски', callback_data='grade_SSSL')
keyboard_test.add(item_Test1)
item_Test2 = types.InlineKeyboardButton(text='📉 Шкала Э. Динера', callback_data='grade_SUZHD')
keyboard_test.add(item_Test2)
item_Test3 = types.InlineKeyboardButton(text='✔ В главное меню', callback_data='menu')
keyboard_test.add(item_Test3)

# Меню для обратной связи (отзыв)
keyboard_claim = types.InlineKeyboardMarkup()
item_Claim1 = types.InlineKeyboardButton(text='ЖКХ', callback_data='claim_zkh')
item_Claim2 = types.InlineKeyboardButton(text='Здоровье', callback_data='claim_health')
item_Claim3 = types.InlineKeyboardButton(text='Образование', callback_data='claim_edu')
keyboard_claim.row(item_Claim1, item_Claim2, item_Claim3)
item_Claim4 = types.InlineKeyboardButton(text='Траспорт', callback_data='claim_trans')
item_Claim5 = types.InlineKeyboardButton(text='Развлечения', callback_data='claim_games')
item_Claim6 = types.InlineKeyboardButton(text='Финансы', callback_data='claim_finance')
keyboard_claim.row(item_Claim4, item_Claim5, item_Claim6)

# Шкала удовлетворенности жизнью Э. Динера
keyboard_SUZHD = types.InlineKeyboardMarkup()
item_SUZHD1 = types.InlineKeyboardButton(text='😭', callback_data='ball1d')
# keyboard_SUZHD.add(item_SUZHD1)  # Полностью не согласен
item_SUZHD2 = types.InlineKeyboardButton(text='😥', callback_data='ball2d')
# keyboard_SUZHD.add(item_SUZHD2)  # Не согласен
item_SUZHD3 = types.InlineKeyboardButton(text='🥺', callback_data='ball3d')
# keyboard_SUZHD.add(item_SUZHD3)  # Скорее не согласен
keyboard_SUZHD.row(item_SUZHD1, item_SUZHD2, item_SUZHD3)
item_SUZHD4 = types.InlineKeyboardButton(text='😐', callback_data='ball4d')
keyboard_SUZHD.add(item_SUZHD4)  # Нечто среднее
item_SUZHD5 = types.InlineKeyboardButton(text='😌', callback_data='ball5d')
# keyboard_SUZHD.add(item_SUZHD5)  # Скорее согласен
item_SUZHD6 = types.InlineKeyboardButton(text='😊', callback_data='ball6d')
# keyboard_SUZHD.add(item_SUZHD6)  # Согласен
item_SUZHD7 = types.InlineKeyboardButton(text='😍', callback_data='ball7d')
# keyboard_SUZHD.add(item_SUZHD7)  # Полностью согласен
keyboard_SUZHD.row(item_SUZHD5, item_SUZHD6, item_SUZHD7)

# Шкала субъективного счастья С.Любомирски
keyboard_SSSL = types.InlineKeyboardMarkup()
item_SSSL1 = types.InlineKeyboardButton(text='😭', callback_data='ball1l')
keyboard_SSSL.row(item_SSSL1)  # Полностью не согласен
item_SSSL2 = types.InlineKeyboardButton(text='😥', callback_data='ball2l')
# keyboard_SSSL.add(item_SSSL2)
item_SSSL3 = types.InlineKeyboardButton(text='🥺', callback_data='ball3l')
# keyboard_SSSL.add(item_SSSL3)
item_SSSL4 = types.InlineKeyboardButton(text='😐', callback_data='ball4l')
# keyboard_SSSL.add(item_SSSL4)
item_SSSL5 = types.InlineKeyboardButton(text='😌', callback_data='ball5l')
# keyboard_SSSL.add(item_SSSL5)
item_SSSL6 = types.InlineKeyboardButton(text='😊', callback_data='ball6l')
# keyboard_SSSL.add(item_SSSL6)
keyboard_SSSL.row(item_SSSL2, item_SSSL3, item_SSSL4, item_SSSL5, item_SSSL6)
item_SSSL7 = types.InlineKeyboardButton(text='😍', callback_data='ball7l')
keyboard_SSSL.row(item_SSSL7)  # Полностью согласен

# Кнопки назад
keyboard_Back = types.InlineKeyboardMarkup()
item1_Back = types.InlineKeyboardButton(text='⬅ Назад к тестам', callback_data='grade_menu')
keyboard_Back.add(item1_Back)
item2_Back = types.InlineKeyboardButton(text='✔ В главное меню', callback_data='menu')
keyboard_Back.add(item2_Back)

# Кнопки выбора шкалы для результата
keyboard_choise_result = types.InlineKeyboardMarkup()
item1_choise_result = types.InlineKeyboardButton(text='📈 По шкале Э.Динера', callback_data='choise_result_diner')
item2_choise_result = types.InlineKeyboardButton(text='📉 По шкале С.Любомирски', callback_data='choise_result_lubomir')
keyboard_choise_result.row(item1_choise_result, item2_choise_result)
item3_choise_result = types.InlineKeyboardButton(text='✔ В главное меню', callback_data='menu')
keyboard_choise_result.add(item3_choise_result)

# Кнопки назад из граф.результата
keyboard_BackGraph = types.InlineKeyboardMarkup()
item1_BackGraph = types.InlineKeyboardButton(text='⬅ Назад к выбору шкалы', callback_data='result_menu')
keyboard_BackGraph.add(item1_BackGraph)
item2_BackGraph = types.InlineKeyboardButton(text='✔ В главное меню', callback_data='menu')
keyboard_BackGraph.add(item2_BackGraph)


# Обработчик текстовых команд
@bot.message_handler(commands=['start', 'grade', 'claim'])
def start_message(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, '☑ Вы находитесь в главном меню чат-бота\nВыберите раздел:',
                         reply_markup=keyboard_Menu)
        # register_new_user(message.from_user.id)
    elif message.text == '/grade':
        bot.send_message(message.chat.id,
                         '💡 Предлагаем поучаствовать в измерении Индекса Счастья\nНо перед этим выберите шкалу:')
        bot.send_message(message.chat.id, 'Выберите тест:', reply_markup=keyboard_test)
    elif message.text == '/claim':
        bot.send_message(message.chat.id, '💬 Чтобы оставить отзыв, выберите категорию обращения:',
                         reply_markup=keyboard_claim)


# Callback-обработчик
@bot.callback_query_handler(func=lambda call: True)
def callback_main(call):
    if call.data == 'menu':
        bot.send_message(call.message.chat.id, '☑ Вы в главном меню!', reply_markup=keyboard_Menu)
    if call.data == 'grade_menu':
        bot.send_message(call.message.chat.id,
                         '💡 Предлагаем поучаствовать в измерении Индекса Счастья\nНо перед этим выберите шкалу:',
                         reply_markup=keyboard_test)
    global SUZHD_start
    global SUZHD_answer
    if call.data == 'grade_SUZHD':
        SUZHD_start = 0
        SUZHD_answer = [0, 0, 0, 0, 0]
        bot.send_message(call.message.chat.id, SUZHD_text)
        bot.send_message(call.message.chat.id, SUZHD_question[SUZHD_start], reply_markup=keyboard_SUZHD)
    if call.data in ['ball1d', 'ball2d', 'ball3d', 'ball4d', 'ball5d', 'ball6d', 'ball7d']:
        if SUZHD_start < 5:
            choise_callback = call.data
            SUZHD_answer[SUZHD_start] = int(choise_callback[4])
            SUZHD_start = SUZHD_start + 1
        if SUZHD_start < 5:
            bot.edit_message_text(chat_id=call.message.chat.id, text=SUZHD_question[SUZHD_start],
                                  message_id=call.message.message_id, reply_markup=keyboard_SUZHD)
        else:
            SUZHD_result = sum(SUZHD_answer)
            bot.send_message(call.message.chat.id,
                             "📌 По шкале удовлетворенности жизнью Э. Динера, ваш результат: " + str(SUZHD_result),
                             reply_markup=keyboard_Back)
            dt_now = datetime.datetime.today()
            result_insert_db(call.message.from_user.id, 1, SUZHD_result, dt_now)
    global SSSL_start
    global SSSL_answer
    if call.data == 'grade_SSSL':
        SSSL_start = 0
        SSSL_answer = [0, 0, 0, 0, 0, 0, 0]
        bot.send_message(call.message.chat.id, SSSL_text)
        bot.send_message(call.message.chat.id, SSSL_question[SSSL_start], reply_markup=keyboard_SSSL)
    if call.data in ['ball1l', 'ball2l', 'ball3l', 'ball4l', 'ball5l', 'ball6l', 'ball7l']:
        if SSSL_start < 7:
            choise_callback = call.data
            SSSL_answer[SSSL_start] = int(choise_callback[4])
            SSSL_start = SSSL_start + 1
        if SSSL_start < 7:
            bot.edit_message_text(chat_id=call.message.chat.id, text=SSSL_question[SSSL_start],
                                  message_id=call.message.message_id, reply_markup=keyboard_SSSL)
        else:
            SSSL_result = sum(SSSL_answer)
            bot.send_message(call.message.chat.id,
                             "📌 По шкале субъективного счастья С.Любомирски, ваш результат: " + str(SSSL_result),
                             reply_markup=keyboard_Back)
            dt_now = datetime.datetime.today()
            result_insert_db(call.message.from_user.id, 2, SSSL_result, dt_now)
    if call.data == 'result_menu':
        bot.send_message(call.message.chat.id, '📊 Чтобы посмотреть результаты, выберите шкалу:',
                         reply_markup=keyboard_choise_result)
    if call.data == 'choise_result_diner':
        bot.send_message(call.message.chat.id, '📈 Ниже представлен график всех ваших тестирований по шкале Э.Динера')
        try:
            photoGraph = open(result_to_graph(call.message.from_user.id, 1), 'rb')
            bot.send_photo(call.message.chat.id, photo=photoGraph)
            bot.send_message(call.message.chat.id, '📊 Чтобы посмотреть результаты, выберите шкалу:',
                             reply_markup=keyboard_choise_result)
        except Exception as e:
            logging.error(str(today) + " " + str(e))
            time.sleep(1)
    if call.data == 'choise_result_lubomir':
        bot.send_message(call.message.chat.id,
                         '📉 Ниже представлен график всех ваших тестирований по шкале С.Любомирски')
        try:
            photoGraph = open(result_to_graph(call.message.from_user.id, 2), 'rb')
            bot.send_photo(call.message.chat.id, photo=photoGraph)
            bot.send_message(call.message.chat.id, '📊 Чтобы посмотреть результаты, выберите шкалу:',
                             reply_markup=keyboard_choise_result)
        except Exception as e:
            logging.error(str(today) + " " + str(e))
            time.sleep(1)


# # Пересылает ошибочные команды увемомляя пользователя об этом
# @bot.message_handler(content_types=['text'], regexp=)
# def default_command(message):
#     bot.reply_to(message, '❌ Нет такой команды!', reply_markup=keyboard_Menu)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("math", math))
    dp.add_handler(CommandHandler("timenow", timenow))


    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=TOKEN)
    updater.bot.setWebhook('https://happyindexbot.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
