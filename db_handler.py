from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

USERNAME = 'postgres'
PASSWORD = 'admin'
HOSTNAME = 'localhost'
PORT = '5432'
DATABASE = 'postgres'

DATABASE_URL=F'postgres://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}'
TABLENAME = 'goo_url_mapping'
ADD_NEW_MAPPING = f"""
INSERT INTO {TABLENAME}(short_url, long_url, owner)
VALUES (:short_url, :long_url, :owner);
"""

GET_MAPPING = f"""
SELECT * 
  FROM {TABLENAME}
 WHERE short_url = :short_url;
"""

REMOVE_MAPPING = f"""
DELETE FROM {TABLENAME}
 WHERE short_url = :short_url;
"""
class DB_Handler(object):
	def __init__(self):
		engine = create_engine(DATABASE_URL)
		self.db = scoped_session(sessionmaker(bind=engine))

	def get_mapping(self, short_url):
		print(f'quering for {short_url} mapping')
		mapping = self.db.execute(GET_MAPPING, {'short_url': short_url}).fetchone()
		if mapping:
			print(f'found {mapping}')
			return mapping
		else:
			print(f'didnt found any..')
			return None
			##TODO:handle execption and raise not found error
	def add_new_mapping(self, short_url, long_url, owner):
		placeholders_dict = {
			'short_url': short_url,
			'long_url': long_url,
			'owner': owner
		}
		self.db.execute(ADD_NEW_MAPPING, placeholders_dict)
		self.db.commit()
		print(f'added new mapping: {placeholders_dict}')
		##TODO:HANDLE EXCEPTIONS WHILE TRYING TOO.

	def remove_mapping(self, short_url):
		self.db.execute(REMOVE_MAPPING, {'short_url': short_url})
		self.db.commit()
		print(f'remove mapping of: {short_url}')
		##TODO: HANDLE EXEPTIONS