from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Mapping(db.Model):
	__tablename__ = 'goo_url_mapping'
	id = db.Column(db.Integer, primary_key=True)
	short_url = db.Column(db.String(), nullable=False, index=True, unique=True)
	long_url = db.Column(db.String(), nullable=False)
	owner = db.Column(db.String(), nullable=True)
	creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

	def __repr__(self):
		return '<Short_url %r>' % self.short_url