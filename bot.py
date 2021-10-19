import telebot
from telebot import types
import speech_recognition as sr
import subprocess as sp
import os

API = os.environ["API"]
bot = telebot.TeleBot(API)
LANGS = {'En': 'en-US',
	     'Ru': 'ru-RU',
	     'Ua': 'uk-UA'}

user_data = {}

@bot.message_handler(commands=['start'])
def get_username(message):
	uname = message.chat.username
	if uname not in user_data:
		user_data[uname] = 'ru-RU'
		
@bot.message_handler(commands=['stop'])
def gremove_username(message):
	try:
		del user_data[message.chat.username]
	except KeyError:
		print("Username does not exist.")

@bot.message_handler(content_types=['voice'])
def process_voice(message):
	r = sr.Recognizer()
	file_info = bot.get_file(message.voice.file_id)
	downloaded_file = bot.download_file(file_info.file_path)
	with open('voice.ogg', 'wb') as new_file:
		new_file.write(downloaded_file)
	process = sp.run(['ffmpeg', '-y', '-loglevel', 'quiet', '-i', 'voice.ogg', 'voice.wav'])
	if process.returncode != 0:
		raise Exception('Something went wrong with audio convertion.')
	with sr.AudioFile('voice.wav') as source:
		audio = r.listen(source)
	text = r.recognize_google(audio, language=user_data[message.chat.username])
	#print(text)
	bot.reply_to(message, text)

@bot.message_handler(commands=['change_lang'])
def change_language(message):
	keyboard = types.InlineKeyboardMarkup()
	key_en = types.InlineKeyboardButton(text='En', callback_data="En")
	keyboard.add(key_en)
	key_ru = types.InlineKeyboardButton(text='Ru', callback_data="Ru")
	keyboard.add(key_ru)
	key_ua = types.InlineKeyboardButton(text='Ua', callback_data="Ua")
	keyboard.add(key_ua)
	msg_text = 'Выберите язык сообщения:'
	bot.send_message(message.from_user.id, text=msg_text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_process(call):
	global user_data
	user_data[call.message.chat.username] = LANGS[call.data]
	bot.send_message(call.message.chat.id, f'Язык изменён на {call.data}.')

bot.polling(none_stop=True, interval=0)
