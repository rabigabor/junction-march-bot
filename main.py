from bottle import run, post, get, request as bottle_request  # <--- we add bottle request
import requests
from io import BytesIO
import numpy as np

import img_generate
import text_generate


BOT_URL = 'https://api.telegram.org/bot<token>/'

HELP_MESSAGE = """Hey there! 🤗

You can use the following commands:
*/motivate* - I'll send you a motivational image with a real quote
*/bullshit* - I'll send you a motivational image with one of my wise thoughts.
*/games* - I'll list you the available games with me to cheer you up."""

ERROR_MESSAGE = """I am sorry but I cannot understand you! 😢

You can use the following commands:
*/motivate* - I'll send you a motivational image with a real quote
*/bullshit* - I'll send you a motivational image with one of my wise thoughts.
*/games* - I'll list you the available games with me to cheer you up. """

GAME_MESSAGE = """You can play the following games with me: 🎮
*/flipacoin {heads|tails}* - Play "Flip a Coin" with me!
*/guess {number}* - I'll think of a random number, you have to guess it.
*/rps {rock|paper|scissors}* - Play "Rock, Paper, Scissors" with me! """


def parse_message(data):
	retval = {}
	if 'message' not in data:
		return None
	retval["chat_id"] = data['message']['chat']['id']
	retval["text"] = data['message']['text']

	return retval

def get_guess_message(msg):
	msg = msg.split(" ")[-1]
	try:
		number = int(msg)
		return np.random.choice(["Almost!", "Not even close.", "A bit higher", "A bit lower", "Come on..", "Really?", "You should give up..", "YESSSSSSSS! Good job!"])
	except:
		return """Sorry, but that's not an integer number! 
Try again with this command: */guess {number}*"""

def get_flip_message(msg):
	if msg == "/flipacoin heads":
		return "Sorry, it was Tails. You've lost.."
	elif msg == "/flipacoin tails":
		return "Sorry, it was Heads. You've lost.."
	else:
		return """You have to pick heads or tails. It is not so hard.. 🤦
Try again with this command: */flipacoin {heads|tails}*"""


def get_rps_message(msg):
	if msg == "/rps rock":
		return "Haha loooser, I've picked paper!"
	elif msg == "/rps paper":
		return "Sorry, I've picked scissors, maybe next time you'll have luck.."
	elif msg == "/rps scissors":
		return "I've picked rock of course, how didn't you know that?!"
	else:
		return """You have to pick rock, paper or scissors. It is not so hard.. 🤦
Try again with this command: */rps {rock|paper|scissors}*"""


def send_message(chat_id, msg):

	json_data = {
		"chat_id": chat_id,
		"text": msg,
		"parse_mode": "Markdown"
	}


	message_url = BOT_URL + 'sendMessage'
	r = requests.post(message_url, json=json_data)
	print(r.status_code, r.reason, r.content)


def generate_photo(message):
	url = "https://source.unsplash.com/640x480?nature"
	response = requests.get(url)


	return img_generate.draw_text_on_image(BytesIO(response.content), message)


def send_motivational_image(chat_id, generate=True):
	
	msg = None
	if generate:
		msg = text_generate.generate_quote()
	else:
		msg = text_generate.pick_random_quote()

	photo_bytes = generate_photo(msg)
	photo = BytesIO(photo_bytes)
	photo.name = 'random_motivational_photo.png'

	files = {'photo': photo}
	json_data = {
		"chat_id": chat_id,
		
	}

	message_url = BOT_URL + 'sendPhoto'
	r = requests.post(message_url, files=files, data=json_data)
	print(" ==== RESPONSE ==== ")
	print(r.status_code, r.reason, r.content)



@post('/')
def main():
	data = parse_message(bottle_request.json)  # <--- extract all request data

	print(" ==== NEW POST REQUEST ==== ")
	print(data)
	if data is None:
		return

	chat_id = data["chat_id"]
	msg = data["text"].lower()

	is_greeting_or_help = False
	for word in ["/start", "help", "hi ", "hey", "hello", "ola", "what's up", "sup"]:
		if word in msg:
			is_greeting_or_help = True


	if is_greeting_or_help:
		send_message(chat_id, HELP_MESSAGE)
	elif "/motivate" == msg:
		send_motivational_image(chat_id, generate=False)
	elif "/bullshit" == msg:
		send_motivational_image(chat_id)
	elif "/games" == msg:
		send_message(chat_id, GAME_MESSAGE)
	elif "/rps" in msg:
		send_message(chat_id, get_rps_message(msg))
	elif "/flipacoin" in msg:
		send_message(chat_id, get_flip_message(msg))
	elif "/guess" in msg:
		send_message(chat_id, get_guess_message(msg))
	else:
		send_message(chat_id, ERROR_MESSAGE)
	return



if __name__ == '__main__':  
	run(host='localhost', port=8080, debug=True, reloader=True)
