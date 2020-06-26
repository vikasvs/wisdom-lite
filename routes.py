from flask import request
from __init__ import app, _update_db
from models import User
from twilio.twiml.messaging_response import MessagingResponse
import db, _update_db
from sqlalchemy import func

def _count_db():
	return db.session.query(User.phone_number).count()

def _send_message(output_lines):
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("\n".join(output_lines))
    return str(resp)



@app.route("/", methods=["POST", "GET"])
def bot():
	output_lines = []
	incoming_msg = request.values.get('Body', '').lower()
	remote_number = request.values.get('From')
	resp = MessagingResponse()
	msg = resp.message()
	responded = False
	user = User.query.get(remote_number)
	

	if incoming_msg == "options":
		output_lines.append("'start' - initialize everything")
		output_lines.append("'fsho' - initialize preset roasts, quotes, and compliments ;)'")
		output_lines.append("'add roast' - save a roast'")
		output_lines.append("'give me a roast' - get a random roast ")
		output_lines.append("'add quote' - save a quote")
		output_lines.append("'give me a quote' - get a random quote")
		output_lines.append("'add compliment' -save a compliment")
		output_lines.append("'give me a compliment' - get a random compliment")
		output_lines.append("'add excuse' - save an excuse to get you out of stuff")
		output_lines.append("'give me an excuse' - get a random excuse")
		output_lines.append("'???' - learn about me")
		output_lines.append("")
		output_lines.append(" if you like wisdom-lite and want to use it fulltime considering venmoing https://venmo.com/code?user_id=2270645291319296805 just 50c!!!!!!. Pls i am not wealthy")
		return _send_message(output_lines)


    # User creation commands
    # - 'create account'

	if not user:
		if incoming_msg == "start":
			new_user = User(remote_number)
			_update_db(new_user)
			add_user(remote_number)
			output_lines.append(
				f"Account successfully created for number {remote_number}!"
			)
			output_lines.append(
				"Text 'options' at any time to see available commands."
			)
			output_lines.append(
				"You wont be able to get any roasts, compliments, quotes, or excuses until you've added an excuse or populated using 'fsho'"
			)
			output_lines.append(
				"wisdom-lite is made for you to remember your greatest quotes, compliments, insults, and save them and relive them in a few texts"
			)
		else:
			output_lines.append("text 'start', first!")

		return _send_message(output_lines)
	else:
		if incoming_msg == "start":
			output_lines.append(f"{remote_number} already setup, text 'options' for options.")
			return _send_message(output_lines)

	#roasts

	if 'fsho' in incoming_msg:
		status = user.load()
		if status:
			output_lines.append("all banks populated with creators's fav's")
		else:
			output_lines.append("could not populate")
		_update_db(user)
		return _send_message(output_lines)

	if "add roast" in incoming_msg:
		output_lines.append("whats the roast?")
		user.add_insult_flag = True
		_update_db(user)
		return _send_message(output_lines)


	if user.add_insult_flag: 
		status = user.add_roast(incoming_msg)
		if status:
			output_lines.append("added")
		else:
			output_lines.append("could not add")
		user.add_insult_flag = False
		_update_db(user)
		return _send_message(output_lines) 


	if "give me a roast" in incoming_msg:
		res = user.get_roast()
		if res is None:
			output_lines.append('no roasts found')
		else:
			output_lines.append(res)
		_update_db(user)
		return _send_message(output_lines) 


	#quotes
	if "add quote" in incoming_msg:
		output_lines.append("whats the quote?")
		user.add_quote_flag = True
		_update_db(user)
		return _send_message(output_lines)


	if user.add_quote_flag: 
		status = user.add_quote(incoming_msg)
		if status:
			output_lines.append("added")
		else:
			output_lines.append("could not add")
		user.add_quote_flag = False
		_update_db(user)
		return _send_message(output_lines) 


	if "give me a quote" in incoming_msg:
		res = user.get_quote()
		if res is None:
			output_lines.append('no quotes found')
		else:
			output_lines.append(res)
		_update_db(user)
		return _send_message(output_lines) 

	#compliments
	if "add compliment" in incoming_msg:
		output_lines.append("whats the compliment?")
		user.add_compliment_flag = True
		_update_db(user)
		return _send_message(output_lines)


	if user.add_compliment_flag: 
		status = user.add_compliment(incoming_msg)
		if status:
			output_lines.append("added")
		else:
			output_lines.append("could not add")
		user.add_compliment_flag = False
		_update_db(user)
		return _send_message(output_lines) 


	if "give me a compliment" in incoming_msg:
		res = user.get_compliment()
		if res is None:
			output_lines.append('no compliments found')
		else:
			output_lines.append(res)
		_update_db(user)
		return _send_message(output_lines) 



	#excuses
	if "add excuse" in incoming_msg:
		output_lines.append("whats the excuse?")
		user.add_excuse_flag = True
		_update_db(user)
		return _send_message(output_lines)


	if user.add_excuse_flag: 
		status = user.add_excuse(incoming_msg)
		if status:
			output_lines.append("added")
		else:
			output_lines.append("could not add")
		user.add_excuse_flag = False
		_update_db(user)
		return _send_message(output_lines) 


	if "give me an excuse" in incoming_msg:
		res = user.get_excuse()
		if res is None:
			output_lines.append('no excuses found')
		else:
			output_lines.append("make sure to change wisdom-lite contact name to the appropriate individual:")
			output_lines.append(res)
		_update_db(user)
		return _send_message(output_lines) 


	if "???" in incoming_msg:
		output_lines.append('vikasvsharma.com')
		return _send_message(output_lines) 

	if "usercount" in incoming_msg:
		output_lines.append(str(_count_db()) + " current users")
		return _send_message(output_lines) 
 


	output_lines.append("Sorry, I don't understand, please try again or text 'options'.")
	return _send_message(output_lines)


if __name__ == "__main__":
    app.run()
