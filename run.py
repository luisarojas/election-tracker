import requests
import time
import json
import random
import smtplib
import ssl
import socket
import sys
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from pathlib import Path
from email.message import EmailMessage

testing_env = False
seconds_to_check = 300  # sleep for 5 minutes before trying again

data_filename = '.db.json'
data = None

def load_prev_db():
	global data
	with open(data_filename) as f:
		data = json.load(f)

def update_db():
	global data
	with open(data_filename, 'w') as f:
		json.dump(data, f)

def check_changes():

	now = datetime.now() - timedelta(hours=5)
	current_time = now.strftime('%b %d, %Y at %I:%M %p EST')

	user_agents = [
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
	]

	headers = {'User-Agent': random.choice(user_agents)}

	url = 'https://abcnews.go.com/Politics/live-updates/2020-election-campaign-vote/?id=73960714'
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'lxml')

	all_counts = soup.select('div.electionCount__voteCountContainer')
	biden_count = int(all_counts[0].text)
	dump_count = int(all_counts[1].text)

	dem_house_count = int(all_counts[4].text)
	gop_house_count = int(all_counts[5].text)

	dem_senate_count = int(all_counts[2].text)
	gop_senate_count = int(all_counts[3].text)

	plain_text_message = ''
	html_message =  ''
	with open('.templates/template.txt') as file: plain_text_message = file.read()
	with open('.templates/template.html') as file: html_message = file.read()

	# Keep track of if any categories have been updated
	data_changed = False
	description_message = ''


	# ------------------------------  Check presidency ------------------------------
	# Biden
	if biden_count != data['president']['Biden']:
		data_changed = True
		description_message = f'{data["president"]["Biden"]} &rarr; {biden_count}'
		data["president"]["Biden"] = biden_count
		html_message = html_message.replace('[biden-color]', 'dem-color') # blue
	else:
		description_message = f'No change ({biden_count})'
		html_message = html_message.replace('[biden-color]', 'no-change-color') # grey

	if (biden_count >= 270): description_message += ' - WIN! 🎉'

	html_message = html_message.replace('[biden-description]', description_message)
	plain_text_message = plain_text_message.replace('[biden-description]', description_message)

	# Dump
	if dump_count != data['president']['Trump']:
		data_changed = True
		description_message = f'{data["president"]["Trump"]} &rarr; {dump_count}'
		html_message = html_message.replace('[dump-color]', 'gop-color') # red
		data["president"]["Trump"] = dump_count
	else:
		description_message = f'No change ({dump_count})'
		html_message = html_message.replace('[dump-color]', 'no-change-color') # grey

	if (dump_count >= 270): description_message += ' - win'

	html_message = html_message.replace('[dump-description]', description_message)
	plain_text_message = plain_text_message.replace('[dump-description]', description_message)



	# ------------------------------ Check house ------------------------------
	# Dem
	if dem_house_count != data['house']['dem']:
		data_changed = True
		description_message = f'{data["house"]["dem"]} &rarr; {dem_house_count}'
		html_message = html_message.replace('[dem-house-color]', 'dem-color') # blue
		data["house"]["dem"] = dem_house_count
	else:
		description_message = f'No change ({dem_house_count})'
		html_message = html_message.replace('[dem-house-color]', 'no-change-color') # grey

	if (dem_house_count >= 218): description_message += ' - MAJORITY! 🎉'

	html_message = html_message.replace('[dem-house-description]', description_message)
	plain_text_message = plain_text_message.replace('[dem-house-description]', description_message)

	# Gop
	if gop_house_count != data['house']['gop']:
		data_changed = True
		description_message = f'{data["house"]["gop"]} &rarr; {gop_house_count}'
		html_message = html_message.replace('[gop-house-color]', 'gop-color') # red
		data["house"]["gop"] = gop_house_count
	else:
		description_message = f'No change ({gop_house_count})'
		html_message = html_message.replace('[gop-house-color]', 'no-change-color') # grey

	if (gop_house_count >= 218): description_message += ' - majority'

	html_message = html_message.replace('[gop-house-description]', description_message)
	plain_text_message = plain_text_message.replace('[gop-house-description]', description_message)



	# ------------------------------ Check senate ------------------------------
	# Dem
	if dem_senate_count != data['senate']['dem']:
		data_changed = True
		description_message = f'{data["senate"]["dem"]} &rarr; {dem_senate_count}'
		html_message = html_message.replace('[dem-senate-color]', 'dem-color') # blue
		data["senate"]["dem"] = dem_senate_count
	else:
		description_message = f'No change ({dem_senate_count})'
		html_message = html_message.replace('[dem-senate-color]', 'no-change-color') # grey

	if (dem_senate_count >= 51): description_message += ' - MAJORITY 🎉'

	html_message = html_message.replace('[dem-senate-description]', description_message)
	plain_text_message = plain_text_message.replace('[dem-senate-description]', description_message)

	# Gop
	if gop_senate_count != data['senate']['gop']:
		data_changed = True
		description_message = f'{data["senate"]["gop"]} &rarr; {gop_senate_count}'
		html_message = html_message.replace('[gop-senate-color]', 'gop-color') # red
		data["senate"]["gop"] = gop_senate_count
	else:
		description_message = f'No change ({gop_senate_count})'
		html_message = html_message.replace('[gop-senate-color]', 'no-change-color') # grey

	if (gop_senate_count >= 51): description_message += ' - majority'

	html_message = html_message.replace('[gop-senate-description]', description_message).replace('[url-source]', url)
	plain_text_message = plain_text_message.replace('[gop-senate-description]', description_message).replace('&rarr;', '->')

	# ------------------------------------------------------------------------------------------

	print(plain_text_message, '\n')

	if data_changed or testing_env:
		if Path('env.py').exists():
			from env import ENV
			try:
				recipient_emails_str = ', '.join(ENV['recipient']['emails'])
				if testing_env: recipient_emails_str = ENV['recipient']['emails'][0]
				print(f'\033[92m*** There are changes ***\033[0m\nSending notification e-mail notification to: {recipient_emails_str}')
			except Exception as e:
				print(e)
				print('Error: Unable to properly read recipient emails from env.py file')
				sys.exit(-1)

			try:
				port = 465  # For SSL
				smtp_server = "smtp.gmail.com"
				sender_email = ENV['sender']['email']
				password = ENV['sender']['password']

				message = EmailMessage()
				subject = '🆕 Election Update'
				if testing_env: subject += ' - Test'
				message['Subject'] = subject
				message['From'] = sender_email
				message['To'] = recipient_emails_str
				message.set_content(plain_text_message)
				message.add_alternative(html_message, subtype='html')

				context = ssl.create_default_context()
				with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
					server.login(sender_email, password)
					server.send_message(message)
			except Exception as e: print(e)

	else: print('*** No changes identified ***')

	print(f'\nRunning every {int(seconds_to_check/60)} minute(s)')
	print(f'Last checked: {current_time}', '\n')

if __name__ == "__main__":

	if testing_env: print('\033[93m\033[1m*** IN TESTING ENVIRONMENT ***\033[0m')

	while True:

		load_prev_db()
		check_changes()
		update_db()

		time.sleep(seconds_to_check)
