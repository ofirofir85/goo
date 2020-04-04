from flask import Flask, render_template, url_for, request, redirect, jsonify, flash
import random
import string
from db_handler import DB_Handler

app = Flask(__name__)
app.secret_key = 'asdm32%$nm$#san12'
app.config['DB_CONNECT_DATA'] = {
	'username': 'postgres',
	'password': 'admin',
	'port': '5432',
	'db_name': 'postgres',
	'hostname': 'localhost',
	'db_type': 'postgres'
}
app.config['DB_TABLENAME'] = 'goo_url_mapping'

db_handler = DB_Handler(app.config['DB_CONNECT_DATA'], app.config['DB_TABLENAME']) #Python class that executs the db queries

@app.route('/')
def home():
	mappings = db_handler.get_user_mappings('test-user')
	return render_template('home.html', mappings=mappings)

@app.route('/check_available', methods=['POST'])
def check_available(): #returns a json answer to ajax request of url availabily
	custom = request.form['custom_url']
	result = {'is_available': is_url_available(custom)}
	return jsonify(result)

def is_url_available(url):# returns if given url already taken.
	mapping = db_handler.get_single_mapping(url)  
	return False if mapping else True

@app.route('/short', methods=['POST'])
def short():#gets the form data and add the short. not validating because it happends on the client side
	short_url = request.form['custom_url'].lstrip()
	long_url = request.form['long_url'].lstrip()
	if short_url == '': #if short_url is empty generate a new url 
		short_url = generate_short_url()
		while (not is_url_available(short_url)):#if generated url is taken, generate until available
			short_url = generate_short_url()
	db_handler.add_new_mapping(short_url,long_url, 'test-user')
	flash(f"Great Success! goo/{short_url} will now redirect to {long_url}",'success')
	return redirect(url_for('home'))

def generate_short_url():#generate a new short url
	chars = list(string.ascii_lowercase + string.digits)
	random.shuffle(chars)
	length = random.randint(3,6)
	return ''.join(chars[:length])

@app.route('/<short_url>')
def redirect_to_long(short_url):#redirecting a short url to its original long url
	mapping = db_handler.get_single_mapping(short_url)
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
	db_handler.remove_mapping(short_url)
	flash(f'Deleted Successfully. {short_url} is now an untaken redirect link.', 'success')
	return redirect(url_for('home'))


if __name__ == '__main__':
	app.run(debug=True)