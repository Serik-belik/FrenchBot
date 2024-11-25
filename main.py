import telebot, json
from telebot import types

bot = telebot.TeleBot('7601716276:AAGQ9fHikwUXNsVDFxsrSRS6BZO28_I1naE')

ChatID = 457274387
Mode = ""
Topic = ""
Questions = list()
QuestionID = int()
i = int()

def select_chapter():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton("Lexic"),
        types.KeyboardButton("Grammaire")
    )
    bot.send_message(ChatID, "Select Mode", reply_markup=markup)

def select_topic():
    files = {"Grammaire": "grammaire.json"}
    with open(files[Mode], encoding='utf-8') as file:
        data = json.load(file)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for key in data.keys():
        markup.add(types.KeyboardButton(key))

    bot.send_message(ChatID, "Select Topic", reply_markup=markup)

def grammaire(message = ""):

    def send_task():
        from random import randint
        global QuestionID
        QuestionID = randint(0, len(Questions) - 1)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for answer in Questions[QuestionID]['V']:
            markup.add(types.KeyboardButton(answer))

        bot.send_message(ChatID, f"{i+1}. {Questions[QuestionID]['Q']}", reply_markup=markup)

    def check_task():
        if message == Questions[QuestionID]['C']:
            bot.send_message(ChatID, 'Correct ', reply_markup=types.ReplyKeyboardRemove())
            del Questions[QuestionID]
            global i
            i += 1
            send_task()
        else:
            bot.send_message(ChatID, 'Incorrect ', reply_markup=types.ReplyKeyboardRemove())
            send_task()

    if not message:
        files = {"Grammaire": "grammaire.json"}
        with open(files[Mode], encoding='utf-8') as file:
            data = json.load(file)[Topic]

        bot.send_message(ChatID, data['Task'], reply_markup=types.ReplyKeyboardRemove())
        global Questions, i
        Questions = data['Questions'].copy()
        i = 0
        send_task()
    else:
        check_task()

@bot.message_handler(commands=['start'])
def main(message):
    select_chapter()

@bot.message_handler()
def message_handler(message):
    global Mode, Topic
    if not Mode:
        Mode = message.text
        select_topic()
    elif not Topic:
        Topic = message.text
        grammaire()
    elif Topic:
        grammaire(message.text)
        if not Questions:
            Topic = ""
            select_topic()


bot.polling()