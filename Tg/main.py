import telebot
import logging
import requests
from dotenv import load_dotenv
import os
from gpt import get_advice

load_dotenv()
API_TOKEN = os.getenv('TOKEN')
speechkit_url = os.getenv('URL')
folder_id = ""
iam_token = os.getenv('TOKEN2')

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
bot = telebot.TeleBot(API_TOKEN, threaded=False)

parasite_dictionary = {
    "мм",
    "типа",
    "вроде",
    "как бы",
    "в общем",
    "ваще",
    "прикинь",
    "итак",
    "короче",
    "вот",
    "кстати",
    "блин",
    "ешкин кот",
    "походу",
    "черт",
    "черт возьми",
    "то есть",
    "ёмаё",
    "жесть",
    "пофиг",
    "в натуре",
    "ну это",
    "эм",
    "хм",
    "ам"
}


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message,
                 "Бот умеет:\n*переводить голосовые сообщения в текст;\n* удалять слова паразиты из сообщения;\n* делать речь чище.")


@bot.message_handler(func=lambda message: True, content_types=['voice'])
def echo_audio(message):
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    response_text = audio_analyze(speechkit_url, iam_token, folder_id, downloaded_file)

    textt = response_text.lower().split()

    count_parasites = sum(1 for word in textt if word in parasite_dictionary)
    cleaned_text = [word for word in textt if word not in parasite_dictionary]
    replaced_text = ' '.join(cleaned_text)
    tep = get_advice(replaced_text)

    reply = (f"Количество слов-паразитов: {count_parasites}"
             f"\nТекст после удаления:\n {tep}")
    bot.reply_to(message, response_text)
    bot.reply_to(message, reply)


def audio_analyze(speechkit_url, iam_token, folder_id, audio_data):
    headers = {'Authorization': f'Api-Key {iam_token}'}
    params = {
        "topic": "general",
        "folderId": f"{folder_id}",
        "lang": "ru-RU"}

    audio_request = requests.post(speechkit_url, params=params, headers=headers, data=audio_data)
    responseData = audio_request.json()
    print(responseData)
    response = 'error'
    if responseData.get("error_code") is None:
        response = (responseData.get("result"))
    return response


@bot.message_handler(func=lambda message: True)
def process_text(message):
    text = message.text.lower().split()

    count_parasites = sum(1 for word in text if word in parasite_dictionary)
    cleaned_text = [word for word in text if word not in parasite_dictionary]
    replaced_text = ' '.join(cleaned_text)

    sentences = replaced_text.split('.')
    final_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        sentence = sentence.capitalize()
        final_sentences.append(sentence)
    final_text = '. '.join(final_sentences)
    final_text = final_text + '.'

    reply = (f"Количество слов-паразитов: {count_parasites}"
             f"\nТекст после удаления:\n {final_text}")
    bot.reply_to(message, reply)


bot.polling()
