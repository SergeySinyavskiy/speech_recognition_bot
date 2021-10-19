import mysql.connector
 
class Base: 
	def __init__(self, db_config_file):
		self.config = db_config_file
		self.connect()
		
	def __del__(self):
		self.cursor.close()
		self.conn.close()

	def connect(self):
		self.conn = mysql.connector.connect(option_files=self.config)
		self.cursor = self.conn.cursor()

	def add_user(self, user_id):
		self.cursor.execute("insert into users (user_id, language) values (%s, %s)", (user_id, 'Ru'))
		self.conn.commit()

	def remove_user(self, user_id):
		self.cursor.execute("delete from users where user_id = %s", (user_id,))
		self.conn.commit()

	def get_user_locale(self, user_id):
		self.cursor.execute("select language from users where user_id = %s", (user_id,))
		lang = self.cursor.fetchone()[0]
		self.cursor.execute("select locale from languages where language like %s", (lang,))
		locale = self.cursor.fetchone()[0]
		return locale

	def change_user_language(self, user_id, lang):
		self.cursor.execute("update users set language = %s where user_id = %s", (lang, user_id))
		self.conn.commit()

	def get_users_list(self):
		self.cursor.execute("select user_id from users")
		return [i[0] for i in self.cursor.fetchall()]
