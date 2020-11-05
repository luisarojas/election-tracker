import requests
import time
import json
import random
import smtplib
import ssl
import socket
from datetime import datetime
from bs4 import BeautifulSoup
from pathlib import Path
from email.message import EmailMessage
from user_agents import USER_AGENTS

testing_env = False

data_filename = '.db.json'
seconds_to_check = 900  # sleep for 15 minutes before trying again
data = None

def load_prev_db():
	global data
	with open(data_filename) as f:
		data = json.load(f)

def update_db():
	global data
	with open(data_filename) as f:
		json.dump(data, f)

def check_changes():

	now = datetime.now()
	current_time = now.strftime('%b %d, %Y at %I:%M %p')

	headers = {'User-Agent': random.choice(USER_AGENTS)}

	url = 'https://abcnews.go.com/Politics/live-updates/2020-election-campaign-vote/?id=73960714'
	page = requests.get(url, headers=headers)
	soup = BeautifulSoup(page.content, 'lxml')

	all_counts = soup.select('div.electionCount__voteCountContainer')
	biden_count = int(all_counts[0].text)
	dump_count = int(all_counts[1].text)
	# print(biden_count, dump_count)

	dem_house_count = int(all_counts[4].text)
	gop_house_count = int(all_counts[5].text)
	# print(dem_house_count, gop_house_count)

	dem_senate_count = int(all_counts[2].text)
	gop_senate_count = int(all_counts[3].text)
	# print(dem_senate_count, gop_senate_count)

	# Check if the numbers have changed
	email_message = ''
	html_email_message = """\
	<!DOCTYPE html>
	<html>
		<head>
			<style>
				@import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');
				body {
				font-family: 'Roboto', sans-serif;
				background-color: white;
				}
				ul {
					font-size: 115%;
					margin-top: 5px;
				}
				h1, p.to-win {
					margin: 0;
				}
			</style>
		</head>
		<body bgcolor=”#ffffff”>
	"""

	# Keep track of if any categories have been updated
	changed = False

	# Check presidency
	email_message += 'Presidency (270 to win)\n' + ("-" *10) + '\n'
	html_email_message += '<h1>Presidency</h1><p class="to-win">270 to win</p><ul>'

	# Biden
	if biden_count != data['president']['Biden']:
		changed = True

		email_message += f'* Biden: {data["president"]["Biden"]} -> {biden_count}'
		html_email_message += f'<li style="color: blue;"><b>Biden</b>: {data["president"]["Biden"]} &rarr; {biden_count}'

		data["president"]["Biden"] = biden_count
	else:
		email_message += f'* Biden: No change ({biden_count})'
		html_email_message += f'<li style="color: grey;"><b>Biden</b>: No change ({biden_count})'
	if (biden_count >= 270):
		email_message += ' - WIN! 🎉'
		html_email_message += ' - WIN! 🎉'
	email_message += '\n'
	html_email_message += '</li>'

	# Dump
	if dump_count != data['president']['Trump']:
		changed = True

		email_message += f'* Trump: {data["president"]["Trump"]} -> {dump_count}'
		html_email_message += f'<li style="color: red;"><b>Trump</b>: {data["president"]["Trump"]} &rarr; {dump_count}'
		
		data["president"]["Trump"] = dump_count
	else:
		email_message += f'* Trump: No change ({dump_count})'
		html_email_message += f'<li style="color: grey;"><b>Trump</b>: No change ({dump_count})'
	if (dump_count >= 270):
		email_message += ' - win'
		html_email_message += ' - win'
	email_message += '\n'
	html_email_message += '</li>'

	html_email_message += '</ul>'

	# Check house
	email_message += '\nHouse (218 for majority)\n' + ("-" *10) + '\n'
	html_email_message += '<h1>House</h1><p class="to-win">218 for majority</p><ul>'

	if dem_house_count != data['house']['dem']:
		changed = True

		email_message += f'* Dem: {data["house"]["dem"]} -> {dem_house_count}'
		html_email_message += f'<li style="color: blue;"><b>Dem</b>: {data["house"]["dem"]} &rarr; {dem_house_count}'

		data["house"]["dem"] = dem_house_count
	else:
		email_message += f'* Dem: No change ({dem_house_count})'
		html_email_message += f'<li style="color: grey;"><b>Dem</b>: No change ({dem_house_count})'
	if (dem_house_count >= 218):
			email_message += ' - MAJORITY!'
			html_email_message += ' - MAJORITY! 🎉'
	email_message += '\n'
	html_email_message += '</li>'
	
	if gop_house_count != data['house']['gop']:
		changed = True

		email_message += f'* Gop: {data["house"]["gop"]} -> {gop_house_count}'
		html_email_message += f'<li style="color: red;"><b>Gop</b>: {data["house"]["gop"]} &rarr; {gop_house_count}'

		data["house"]["gop"] = gop_house_count
	else:
		email_message += f'* Gop: No change ({gop_house_count})'
		html_email_message += f'<li style="color: grey;"><b>Gop</b>: No change ({gop_house_count})'
	if (gop_house_count >= 218):
			email_message += ' - majority'
			html_email_message += ' - majority'
	email_message += '\n'
	html_email_message += '</li>'
	html_email_message += '</ul>'

	# Check senate
	email_message += '\nSenate (51 for majority)\n' + ("-" *10) + '\n'
	html_email_message += '<h1>Senate</h1><p class="to-win">51 for majority</p><ul>'

	if dem_senate_count != data['senate']['dem']:
		changed = True

		email_message += f'* Dem: {data["senate"]["dem"]} -> {dem_senate_count}'
		html_email_message += f'<li style="color: blue;"><b>Dem</b>: {data["senate"]["dem"]} &rarr; {dem_senate_count}'
		
		data["senate"]["dem"] = dem_senate_count
	else:
		email_message += f'* Dem: No change ({dem_senate_count})'
		html_email_message += f'<li style="color: grey;"><b>Dem</b>: No change ({dem_senate_count})'
	if (dem_senate_count >= 51):
		email_message += ' - MAJORITY!'
		html_email_message += ' - MAJORITY 🎉'	
	email_message += '\n'
	html_email_message += '</li>'

	if gop_senate_count != data['senate']['gop']:
		changed = True

		email_message += f'* Gop: {data["senate"]["gop"]} -> {gop_senate_count}'
		html_email_message += f'<li style="color: red;"><b>Gop</b>: {data["senate"]["gop"]} &rarr; {gop_senate_count}'
		
		data["senate"]["gop"] = gop_senate_count
	else:
		email_message += f'* Gop: No change ({gop_senate_count})'
		html_email_message += f'<li style="color: grey;"><b>Gop</b>: No change ({gop_senate_count})'
	if (gop_senate_count >= 51):
		email_message += ' - majority'
		html_email_message += ' - majority'
	email_message += '\n'
	html_email_message += '</li>'
	html_email_message += '</ul>'

	print(email_message)
	html_email_message += f"""\
	<p style="color: grey; margin-top: 25px;">Visit source <a target="_blank" href="{url}">here</a></p>
	</body>
	</html>
	"""

	if changed or testing_env:
		try:
			if Path('env.py').exists():
				from env import ENV

				recipient_emails_str = ', '.join(ENV['recipient']['emails'])
				if testing_env: recipient_emails_str = ENV['recipient']['emails'][0]
				print(f'There are changes\nSending notification e-mail notification to: {recipient_emails_str}')
				
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
				message.set_content(email_message)
				message.add_alternative(html_email_message, subtype='html')

				context = ssl.create_default_context()
				with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
					server.login(sender_email, password)
					server.send_message(message)

		except Exception as e: print('\n', e) # No biggie if the e-mail is not sent

	else: print('--> No changes <--')

	print(f'\nRunning every {int(seconds_to_check/60)} minute(s)')
	print(f'Last checked: {current_time}', '\n')

if __name__ == "__main__":

	if testing_env:
		print('\033[93m*** IN TESTING ENVIRONMENT ***\033[0m')
	
	while True:

		load_prev_db()
		check_changes()
		update_db()

		time.sleep(seconds_to_check)