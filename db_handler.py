from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import current_app

ADD_NEW_MAPPING = """
INSERT INTO {tablename}(short_url, long_url, owner)
VALUES (:short_url, :long_url, :owner);
"""

GET_SINGLE_MAPPING = """
SELECT * 
  FROM {tablename}
 WHERE short_url = :short_url;
"""

REMOVE_MAPPING = """
DELETE FROM {tablename}
 WHERE short_url = :short_url;
"""

GET_USER_MAPPINGS = """
SELECT *
  FROM {tablename}
 WHERE owner = :user
"""

class DB_Handler(object):
	def __init__(self, connect_data, tablename):
		self.tablename = tablename
		connect_data = connect_data
		username = connect_data['username']
		password = connect_data['password']
		hostname = connect_data['hostname']
		port = connect_data['port']
		database = connect_data['db_name']
		db_type = connect_data['db_type']
		database_url=f'{db_type}://{username}:{password}@{hostname}:{port}/{database}'
		engine = create_engine(database_url)
		self.db = scoped_session(sessionmaker(bind=engine))

	def get_single_mapping(self, short_url):
		print(f'quering for {short_url} mapping')
		mapping = self.db.execute(GET_SINGLE_MAPPING.format(tablename=self.tablename), {'short_url': short_url}).fetchone()
		if mapping:
			print(f'found {mapping}')
			return mapping
		else:
			print(f'didnt found mapping')
			return None
			##TODO:handle execption and raise not found error
	def add_new_mapping(self, short_url, long_url, owner):
		placeholders_dict = {
			'short_url': short_url,
			'long_url': long_url,
			'owner': owner
		}
		self.db.execute(ADD_NEW_MAPPING.format(tablename=self.tablename), placeholders_dict)
		self.db.commit()
		print(f'added new mapping: {placeholders_dict}')
		##TODO:HANDLE EXCEPTIONS WHILE TRYING TOO.

	def remove_mapping(self, short_url):
		self.db.execute(REMOVE_MAPPING.format(tablename=self.tablename), {'short_url': short_url})
		self.db.commit()
		print(f'remove mapping of: {short_url}')
		##TODO: HANDLE EXEPTIONS

	def get_user_mappings(self, user):
		mappings = self.db.execute(GET_USER_MAPPINGS.format(tablename=self.tablename), {'user': user}).fetchall()
		return mappings