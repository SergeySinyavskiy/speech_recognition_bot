import mysql.connector

class Base:
	def __init__(self, db_config_file):
		self.config = db_config_file

	def connect(self):
		self.conn = mysql.connector.connect(option_files=self.config)
		self.cursor = self.conn.cursor()
		
	def add_user(self, user_id):
		
	def remove_user(self, user_id):
		
	def get_user_language(self, user_id):
		
	def change_user_language(self, user_id, lang):
		
	def get_users_list(self):
		
		
	#todo: create tables for langs and users 
	#      implement methods
