from flask import Flask, render_template, url_for, request, redirect, jsonify
import random
import string
from db_handler import DB_Handler
app = Flask(__name__)
url_mapping = {}

@app.route('/')
def home():
	return render_template('home.html')

db_handler = DB_Handler()

@app.route('/check_available', methods=['POST'])
def check_available():
	custom = request.form['custom_url']
	result = {'is_available': is_url_available(custom)}
	return jsonify(result)

def is_url_available(url):
	mapping = db_handler.get_mapping(url) 
	return False if mapping else True

@app.route('/short', methods=['POST'])
def short():
	short_url = request.form['custom_url'].lstrip()
	long_url = request.form['long_url'].lstrip()
	if short_url == '':
		short_url = generate_short_url()
		while (not is_url_available(short_url)):
			short_url = generate_short_url()
	db_handler.add_new_mapping(short_url,long_url, 'test-user')
	return f'goo/{short_url} will now redirect to {long_url}'
		

def generate_short_url():
	chars = list(string.ascii_lowercase + string.digits)
	random.shuffle(chars)
	length = random.randint(3,6)
	return ''.join(chars[:length])

@app.route('/<short_url>')
def redirect_to_long(short_url):

	mapping = db_handler.get_mapping(short_url)
	if mapping:
		print(f'redirecting {short_url} to {mapping.long_url}')
		return redirect(mapping.long_url)
	else:
		print(f'goo/{short_url} doesnt exits')
		return redirect(url_for('home'))
		##TODO:ADD MESSEGE FOR NOT EXISTING REDIRECTION
		

if __name__ == '__main__':
	app.run(debug=True)