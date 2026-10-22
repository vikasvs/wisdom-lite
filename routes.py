from flask import request, current_app
from __init__ import app, _update_db, db
from models import User
from twilio.twiml.messaging_response import MessagingResponse
from twilio.request_validator import RequestValidator
from functools import wraps


def validate_twilio_request(f):
    """Decorator to validate Twilio request signatures"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip validation in development or test mode
        if current_app.config.get('DEBUG') or current_app.config.get('TESTING'):
            return f(*args, **kwargs)
        
        validator = RequestValidator(current_app.config['TWILIO_AUTH_TOKEN'])
        
        url = request.url
        params = request.form
        signature = request.headers.get('X-Twilio-Signature', '')
        
        if not validator.validate(url, params, signature):
            return "Invalid request signature", 403
            
        return f(*args, **kwargs)
    return decorated_function


def _count_db():
    return db.session.query(User.phone_number).count()


def _send_message(output_lines):
    resp = MessagingResponse()
    msg = resp.message()
    msg.body("\n".join(output_lines))
    return str(resp)


# Command handlers
def handle_options(user, incoming_msg):
    """Display available commands"""
    output_lines = [
        "'start' - initialize everything",
        "'fsho' - initialize preset roasts, quotes, and compliments",
        "'add roast' - save a roast",
        "'give me a roast' - get a random roast",
        "'add quote' - save a quote",
        "'give me a quote' - get a random quote",
        "'add compliment' - save a compliment",
        "'give me a compliment' - get a random compliment",
        "'add excuse' - save an excuse",
        "'give me an excuse' - get a random excuse",
        "'???' - learn about me",
        "",
        "If you like wisdom-lite and want to support it, consider venmoing https://venmo.com/code?user_id=2270645291319296805"
    ]
    return _send_message(output_lines)


def handle_start(user, incoming_msg):
    """Handle account creation"""
    remote_number = request.values.get('From')
    
    if user:
        return _send_message([f"{remote_number} already setup, text 'options' for options."])
    
    new_user = User(remote_number)
    _update_db(new_user)
    
    output_lines = [
        f"Account successfully created for number {remote_number}!",
        "Text 'options' at any time to see available commands.",
        "You won't be able to get any roasts, compliments, quotes, or excuses until you've added them or populated using 'fsho'",
        "wisdom-lite is made for you to remember your greatest quotes, compliments, insults, and save them and relive them in a few texts"
    ]
    return _send_message(output_lines)


def handle_fsho(user, incoming_msg):
    """Load preset content"""
    if not user:
        return _send_message(["Text 'start' first!"])
    
    status = user.load()
    if status:
        return _send_message(["All banks populated with creator's favorites"])
    return _send_message(["Could not populate"])


def handle_add_roast(user, incoming_msg):
    """Start roast addition flow"""
    if not user:
        return _send_message(["Text 'start' first!"])
    
    user.add_insult_flag = True
    _update_db(user)
    return _send_message(["What's the roast?"])


def handle_get_roast(user, incoming_msg):
    """Get a random roast"""
    if not user:
        return _send_message(["Text 'start' first!"])
    
    res = user.get_roast()
    if res is None:
        return _send_message(['No roasts found. Add some with "add roast" or load presets with "fsho"'])
    return _send_message([res])


def handle_add_quote(user, incoming_msg):
    """Start quote addition flow"""
    if not user:
        return _send_message(["Text 'start' first!"])
    
    user.add_quote_flag = True
    _update_db(user)
    return _send_message(["What's the quote?"])


def handle_get_quote(user, incoming_msg):
    """Get a random quote"""
    if not user:
        return _send_message(["Text 'start' first!"])
    
    res = user.get_quote()
    if res is None:
        return _send_message(['No quotes found. Add some with "add quote" or load presets with "fsho"'])
    return _send_message([res])


def handle_add_compliment(user, incoming_msg):
    """Start compliment addition flow"""
    if not user:
        return _send_message(["Text 'start' first!"])
    
    user.add_compliment_flag = True
    _update_db(user)
    return _send_message(["What's the compliment?"])


def handle_get_compliment(user, incoming_msg):
    """Get a random compliment"""
    if not user:
        return _send_message(["Text 'start' first!"])
    
    res = user.get_compliment()
    if res is None:
        return _send_message(['No compliments found. Add some with "add compliment" or load presets with "fsho"'])
    return _send_message([res])


def handle_add_excuse(user, incoming_msg):
    """Start excuse addition flow"""
    if not user:
        return _send_message(["Text 'start' first!"])
    
    user.add_excuse_flag = True
    _update_db(user)
    return _send_message(["What's the excuse?"])


def handle_get_excuse(user, incoming_msg):
    """Get a random excuse"""
    if not user:
        return _send_message(["Text 'start' first!"])
    
    res = user.get_excuse()
    if res is None:
        return _send_message(['No excuses found. Add some with "add excuse" or load presets with "fsho"'])
    
    return _send_message([
        "Make sure to change wisdom-lite contact name to the appropriate individual:",
        res
    ])


def handle_about(user, incoming_msg):
    """Show about information"""
    return _send_message(['vikasvsharma.com'])


def handle_usercount(user, incoming_msg):
    """Show user count"""
    return _send_message([f"{_count_db()} current users"])


# Command table - maps command keywords to handler functions
COMMANDS = {
    'options': handle_options,
    'start': handle_start,
    'fsho': handle_fsho,
    'add roast': handle_add_roast,
    'give me a roast': handle_get_roast,
    'add quote': handle_add_quote,
    'give me a quote': handle_get_quote,
    'add compliment': handle_add_compliment,
    'give me a compliment': handle_get_compliment,
    'add excuse': handle_add_excuse,
    'give me an excuse': handle_get_excuse,
    '???': handle_about,
    'usercount': handle_usercount,
}


@app.route("/", methods=["POST", "GET"])
@validate_twilio_request
def bot():
    """Main bot endpoint"""
    incoming_msg = request.values.get('Body', '').lower()
    remote_number = request.values.get('From')
    user = db.session.get(User, remote_number)
    
    # Handle flag-based flows (user is adding content)
    if user:
        if user.add_insult_flag:
            status = user.add_roast(incoming_msg)
            user.add_insult_flag = False
            _update_db(user)
            return _send_message(["Added" if status else "Could not add"])
        
        if user.add_quote_flag:
            status = user.add_quote(incoming_msg)
            user.add_quote_flag = False
            _update_db(user)
            return _send_message(["Added" if status else "Could not add"])
        
        if user.add_compliment_flag:
            status = user.add_compliment(incoming_msg)
            user.add_compliment_flag = False
            _update_db(user)
            return _send_message(["Added" if status else "Could not add"])
        
        if user.add_excuse_flag:
            status = user.add_excuse(incoming_msg)
            user.add_excuse_flag = False
            _update_db(user)
            return _send_message(["Added" if status else "Could not add"])
    
    # Look up command in command table
    for command_key, handler in COMMANDS.items():
        if command_key in incoming_msg:
            return handler(user, incoming_msg)
    
    # Default response
    return _send_message(["Sorry, I don't understand. Please try again or text 'options'."])


if __name__ == "__main__":
    app.run()
