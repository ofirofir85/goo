from flask import Flask, render_template, url_for, request, redirect, jsonify
from validators import url as is_valid_url
import random
import string
app = Flask(__name__)
url_mapping = {}

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/check_available', methods=['POST'])
def check_available():
	custom = request.form['custom_url']
	result = {'is_available': is_url_available(custom)}
	return jsonify(result)

def is_url_available(url):
	return False if url in url_mapping else True

@app.route('/short', methods=['POST'])
def short():
	short_url = request.form['custom_url'].lstrip()
	original_url = request.form['original_url'].lstrip()
	if short_url == '':
		short_url = generate_short_url()
		while (not is_url_available(short_url)):
			short_url = generate_short_url()
	add_new_short(short_url, original_url)
	return f'goo/{short_url} will now redirect to {original_url}'

def add_new_short(short_url, original_url):
	url_mapping[short_url] = original_url
	print(url_mapping)

def get_original_url(short_url):
		if short_url in url_mapping:
			return url_mapping[short_url]
		return ''

def generate_short_url():
	chars = list(string.ascii_lowercase + string.digits)
	random.shuffle(chars)
	length = random.randint(3,6)
	return ''.join(chars[:length])

@app.route('/<short_url>')
def redirect_to_original(short_url):

	long_url = get_original_url(short_url)
	if long_url == '':
		print(f'goo/{short_url} doesnt exits')
		return redirect(url_for('home'))
	else:
		print(f'redirecting {short_url} to {long_url}')
		return redirect(long_url)

if __name__ == '__main__':
	app.run(debug=True)