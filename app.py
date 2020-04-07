from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
import random
import string
from models import *

app = Flask(__name__)
app.secret_key = 'asdm32%$nm$#san12'
USERNAME = 'postgres'
PASSWORD = 'admin'
PORT = '5432'
DB_NAME = 'postgres'
HOSTNAME = 'localhost'
DB_TYPE = 'postgres'
app.config['SQLALCHEMY_DATABASE_URI'] = f'{DB_TYPE}://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def home():
	mappings = Mapping.query.filter_by(owner = 'test-user').all()
	return render_template('home.html', mappings=mappings)
	

@app.route('/check_available', methods=['POST'])
def check_available(): #returns a json answer to ajax request of url availabily
	custom = request.form['custom_url']
	result = {'is_available': is_url_available(custom)}
	return jsonify(result)

def is_url_available(url):# returns if given url already taken. 
	mapping = Mapping.query.filter_by(short_url = url).first()
	return False if mapping else True

@app.route('/short', methods=['POST'])
def short():#gets the form data and add the short. not validating because it happends on the client side
	short_url = request.form['custom_url'].lstrip()
	long_url = request.form['long_url'].lstrip()
	if short_url == '': #if short_url is empty generate a new url 
		short_url = generate_short_url()
		while (not is_url_available(short_url)):#if generated url is taken, generate until available
			short_url = generate_short_url()
	mapping = Mapping(short_url=short_url, long_url=long_url, owner='test-user')
	db.session.add(mapping)
	db.session.commit()
	flash(f"Great Success! goo/{short_url} will now redirect to {long_url}",'success')
	return redirect(url_for('home'))

def generate_short_url():#generate a new short url
	chars = list(string.ascii_lowercase + string.digits)
	random.shuffle(chars)
	length = random.randint(3,6)
	return ''.join(chars[:length])

@app.route('/<short_url>')
def redirect_to_long(short_url):#redirecting a short url to its original long url
	mapping = Mapping.query.filter_by(short_url = short_url).first()
	if mapping:
		print(f'redirecting {short_url} to {mapping.long_url}')
		return redirect(mapping.long_url)
	else:
		print(f'goo/{short_url} doesnt exits')
		flash(f'Oops! goo/{short_url} does not exist.. Use this short for your long URL down below!', 'warning')
		return redirect(url_for('home'))
		
@app.route('/remove', methods=['POST'])
def remove():#removes a url mapping after delete button pressed
	short_url = request.form['delete']
	mapping = Mapping.query.filter_by(short_url = short_url).first()
	db.session.delete(mapping)
	db.session.commit()
	flash(f'Deleted Successfully. {short_url} is now an untaken redirect link.', 'success')
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)