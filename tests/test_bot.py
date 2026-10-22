"""
Tests for wisdom-lite SMS bot

Run with: pytest tests/
"""

import pytest
from __init__ import app, db
from models import User, SavedItem


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


@pytest.fixture
def test_phone():
    """Test phone number"""
    return '+15551234567'


def send_sms(client, phone, message):
    """Helper to send SMS message"""
    return client.post('/', data={
        'From': phone,
        'Body': message
    })


def test_options_command(client, test_phone):
    """Test the options command"""
    response = send_sms(client, test_phone, 'options')
    assert response.status_code == 200
    assert b'start' in response.data
    assert b'add roast' in response.data
    assert b'add quote' in response.data


def test_start_command_creates_user(client, test_phone):
    """Test that start command creates a new user"""
    response = send_sms(client, test_phone, 'start')
    assert response.status_code == 200
    assert b'Account successfully created' in response.data
    
    # Verify user exists in database
    with app.app_context():
        user = db.session.get(User, test_phone)
        assert user is not None
        assert user.phone_number == test_phone


def test_start_command_existing_user(client, test_phone):
    """Test that start command handles existing user"""
    # Create user first
    send_sms(client, test_phone, 'start')
    
    # Try to start again
    response = send_sms(client, test_phone, 'start')
    assert response.status_code == 200
    assert b'already setup' in response.data


def test_fsho_command_loads_presets(client, test_phone):
    """Test that fsho command loads preset content"""
    # Create user
    send_sms(client, test_phone, 'start')
    
    # Load presets
    response = send_sms(client, test_phone, 'fsho')
    assert response.status_code == 200
    assert b'populated' in response.data
    
    # Verify items were added
    with app.app_context():
        user = db.session.get(User, test_phone)
        assert len(user.saved_items) > 0


def test_add_and_get_roast(client, test_phone):
    """Test adding and retrieving a roast"""
    # Create user
    send_sms(client, test_phone, 'start')
    
    # Start adding roast
    response = send_sms(client, test_phone, 'add roast')
    assert response.status_code == 200
    assert b"What's the roast?" in response.data
    
    # Add the roast
    test_roast = "You're as useful as a screen door on a submarine"
    response = send_sms(client, test_phone, test_roast)
    assert response.status_code == 200
    assert b'Added' in response.data
    
    # Get the roast back
    response = send_sms(client, test_phone, 'give me a roast')
    assert response.status_code == 200
    assert test_roast.lower().encode() in response.data


def test_add_and_get_quote(client, test_phone):
    """Test adding and retrieving a quote"""
    send_sms(client, test_phone, 'start')
    
    # Add quote
    send_sms(client, test_phone, 'add quote')
    test_quote = "Life is what happens when you're busy making other plans"
    response = send_sms(client, test_phone, test_quote)
    assert b'Added' in response.data
    
    # Get quote
    response = send_sms(client, test_phone, 'give me a quote')
    assert test_quote.lower().encode() in response.data


def test_add_and_get_compliment(client, test_phone):
    """Test adding and retrieving a compliment"""
    send_sms(client, test_phone, 'start')
    
    # Add compliment
    send_sms(client, test_phone, 'add compliment')
    test_compliment = "You are an amazing person!"
    response = send_sms(client, test_phone, test_compliment)
    assert b'Added' in response.data
    
    # Get compliment
    response = send_sms(client, test_phone, 'give me a compliment')
    assert test_compliment.lower().encode() in response.data


def test_add_and_get_excuse(client, test_phone):
    """Test adding and retrieving an excuse"""
    send_sms(client, test_phone, 'start')
    
    # Add excuse
    send_sms(client, test_phone, 'add excuse')
    test_excuse = "My cat is sick and needs to go to the vet"
    response = send_sms(client, test_phone, test_excuse)
    assert b'Added' in response.data
    
    # Get excuse
    response = send_sms(client, test_phone, 'give me an excuse')
    assert test_excuse.lower().encode() in response.data


def test_get_empty_roast_list(client, test_phone):
    """Test getting roast when list is empty"""
    send_sms(client, test_phone, 'start')
    
    response = send_sms(client, test_phone, 'give me a roast')
    assert response.status_code == 200
    assert b'No roasts found' in response.data


def test_get_empty_quote_list(client, test_phone):
    """Test getting quote when list is empty"""
    send_sms(client, test_phone, 'start')
    
    response = send_sms(client, test_phone, 'give me a quote')
    assert response.status_code == 200
    assert b'No quotes found' in response.data


def test_get_empty_compliment_list(client, test_phone):
    """Test getting compliment when list is empty"""
    send_sms(client, test_phone, 'start')
    
    response = send_sms(client, test_phone, 'give me a compliment')
    assert response.status_code == 200
    assert b'No compliments found' in response.data


def test_get_empty_excuse_list(client, test_phone):
    """Test getting excuse when list is empty"""
    send_sms(client, test_phone, 'start')
    
    response = send_sms(client, test_phone, 'give me an excuse')
    assert response.status_code == 200
    assert b'No excuses found' in response.data


def test_about_command(client, test_phone):
    """Test the about command"""
    response = send_sms(client, test_phone, '???')
    assert response.status_code == 200
    assert b'vikasvsharma.com' in response.data


def test_usercount_command(client, test_phone):
    """Test the usercount command"""
    # Create a user
    send_sms(client, test_phone, 'start')
    
    response = send_sms(client, test_phone, 'usercount')
    assert response.status_code == 200
    assert b'1 current users' in response.data


def test_invalid_command(client, test_phone):
    """Test handling of invalid command"""
    send_sms(client, test_phone, 'start')
    
    response = send_sms(client, test_phone, 'this is not a valid command')
    assert response.status_code == 200
    assert b"don't understand" in response.data


def test_command_without_start(client, test_phone):
    """Test that commands require start first"""
    response = send_sms(client, test_phone, 'add roast')
    assert response.status_code == 200
    assert b"start" in response.data.lower()


def test_saved_item_model(client, test_phone):
    """Test SavedItem model functionality"""
    with app.app_context():
        # Create user
        user = User(test_phone)
        db.session.add(user)
        db.session.commit()
        
        # Add items
        user.add_roast("Test roast")
        user.add_quote("Test quote")
        db.session.commit()
        
        # Verify items exist
        roast_items = SavedItem.query.filter_by(user_id=test_phone, kind='roast').all()
        quote_items = SavedItem.query.filter_by(user_id=test_phone, kind='quote').all()
        
        assert len(roast_items) == 1
        assert len(quote_items) == 1
        assert roast_items[0].text == "Test roast"
        assert quote_items[0].text == "Test quote"
