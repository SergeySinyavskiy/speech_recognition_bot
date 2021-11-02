import telebot
from telebot import types
import speech_recognition as sr
import subprocess as sp
import os

API = os.environ["API"]
bot = telebot.TeleBot(API)
LANGS = {'EN': 'en-US',
	     'RU': 'ru-RU',
	     'UA': 'uk-UA'}

user_data = {}

@bot.message_handler(commands=['start']) ### Start script of bot that reads user id and add it to the database
def get_username(message):
	uname = message.chat.username
	if uname not in user_data: 
		user_data[uname] = 'ru-RU' ### Default lang parameter for bot translations if userid is new for bot and wasn't met yet
		
@bot.message_handler(commands=['stop']) ### Stop script for bot that deletes user id of current user who working with bot from database
def remove_username(message):
	try:
		del user_data[message.chat.username]
	except KeyError:
		print("Username does not exist.")

@bot.message_handler(content_types=['voice']) ### Bot script that reads the content of a message. Downloading it and convert it into text representation.
def process_voice(message):
	rec = sr.Recognizer()
	file_info = bot.get_file(message.voice.file_id) ### download audio file
	downloaded_file = bot.download_file(file_info.file_path) ### Open file and convert it in ogg format
	with open('voice.ogg', 'wb') as new_file:
		new_file.write(downloaded_file)
	process = sp.run(['ffmpeg', '-y', '-loglevel', 'quiet', '-i', 'voice.ogg', 'voice.wav']) ### conver process
	if process.returncode != 0:
		raise Exception('Something went wrong with audio convertion.')
	with sr.AudioFile('voice.wav') as source:
		audio = rec.listen(source) ### Parse audio file
	text = rec.recognize_google(audio, language=user_data[message.chat.username]) ### Translate audio file in accordance with lang parameter
	bot.reply_to(message, text) ### Bot reply to user 

@bot.message_handler(commands=['change_lang']) ### Change language buttons menu
def change_language(message):
	keyboard = types.InlineKeyboardMarkup()
	key_en = types.InlineKeyboardButton(text='EN', callback_data="EN")
	keyboard.add(key_en)
	key_ru = types.InlineKeyboardButton(text='RU', callback_data="RU")
	keyboard.add(key_ru)
	key_ua = types.InlineKeyboardButton(text='UA', callback_data="UA")
	keyboard.add(key_ua)
	msg_text = 'Выберите язык сообщения:'
	bot.send_message(message.from_user.id, text=msg_text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_process(call):
	global user_data
	user_data[call.message.chat.username] = LANGS[call.data]
	bot.send_message(call.message.chat.id, f'Язык изменён на {call.data}.')

bot.polling(none_stop=True, interval=0)

#Launch http server for listening port
import socketserver
PORT = int(os.environ.get('PORT'))
from http.server import HTTPServer, BaseHTTPRequestHandler
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'No Memes Today :c')

with socketserver.TCPServer(("0.0.0.0", PORT), SimpleHTTPRequestHandler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()