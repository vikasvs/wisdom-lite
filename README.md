# wisdom-lite

A personalized SMS bot that provides advice, quotes, excuses, roasts, and compliments via text message. Built with Flask and Twilio.

Wisdom-lite remembers your favorite compliments, advice, quotes, roasts, and excuses, and gives them back to you on demand via SMS. Can't think of any content? Load presets with the `fsho` command to get started with curated content.

## Features

- 📱 SMS-based interaction via Twilio
- 💾 Personal database of quotes, roasts, compliments, and excuses
- 🎲 Random retrieval of saved content
- 🎁 Preset content banks to get started quickly
- 🔒 Secure configuration with environment variables
- ✅ Request signature validation for security
- 🧪 Comprehensive test suite

## Requirements

- Python 3.12+
- Twilio account with phone number
- PostgreSQL or SQLite database

## Installation

1. Clone the repository:

```bash
git clone https://github.com/vikasvs/wisdom-lite.git
cd wisdom-lite
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure it:

```bash
cp .env.example .env
```

5. Edit `.env` and add your configuration:

```bash
# Flask Configuration
SECRET_KEY=your-secret-key-here-use-a-random-string
FLASK_ENV=development
DEBUG=False

# Database
DATABASE_URL=sqlite:///app.db  # Or PostgreSQL URL for production

# Twilio Configuration
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
```

6. Initialize the database:

```bash
flask db upgrade
```

7. Run the application:

```bash
# Development
python main.py

# Production (with Gunicorn)
gunicorn __init__:app
```

## Configuration

### Generating a Secret Key

Generate a secure random secret key:

```bash
python -c 'import secrets; print(secrets.token_hex(32))'
```

### Twilio Setup

1. Sign up for a Twilio account at https://www.twilio.com
2. Get a Twilio phone number
3. Configure the webhook URL for your phone number to point to `https://your-domain.com/` (POST)
4. Copy your Account SID and Auth Token to `.env`

## Usage

Text your Twilio number to interact with wisdom-lite:

### Getting Started

- `start` - Initialize your account
- `options` - See all available commands

### Managing Content

- `fsho` - Load preset content (quotes, roasts, compliments, excuses)
- `add roast` - Save a new roast
- `add quote` - Save a new quote
- `add compliment` - Save a new compliment
- `add excuse` - Save a new excuse

### Retrieving Content

- `give me a roast` - Get a random roast
- `give me a quote` - Get a random quote
- `give me a compliment` - Get a random compliment
- `give me an excuse` - Get a random excuse

### Other Commands

- `???` - Learn about the creator
- `usercount` - See how many users are registered

## Running Tests

Run the test suite with pytest:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_bot.py

# Run with verbose output
pytest -v
```

## Database Migrations

Create a new migration after model changes:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Deployment

### Heroku

1. Install the Heroku CLI
2. Create a new Heroku app:

```bash
heroku create your-app-name
```

3. Add PostgreSQL:

```bash
heroku addons:create heroku-postgresql:mini
```

4. Set environment variables:

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set TWILIO_ACCOUNT_SID=your-sid
heroku config:set TWILIO_AUTH_TOKEN=your-token
heroku config:set TWILIO_PHONE_NUMBER=your-number
```

5. Deploy:

```bash
git push heroku master
```

6. Initialize the database:

```bash
heroku run flask db upgrade
```

## Security

This application implements several security best practices:

- ✅ No hardcoded secrets
- ✅ Environment-based configuration
- ✅ Twilio request signature validation
- ✅ Proper `.gitignore` to prevent secret commits
- ✅ Debug mode disabled by default
- ✅ Secure session management

## Architecture

- **Flask 3.0** - Web framework
- **SQLAlchemy 2.0** - ORM for database operations
- **Twilio 9.3** - SMS messaging
- **pytest** - Testing framework

### Database Models

- `User` - Stores user phone numbers and state flags
- `SavedItem` - Stores user content (quotes, roasts, etc.) with timestamps

## Development

### Project Structure

```
wisdom-lite/
├── __init__.py          # Flask app initialization
├── config.py            # Configuration management
├── models.py            # Database models
├── routes.py            # Route handlers and bot logic
├── presets.py           # Preset content banks
├── main.py              # Development entry point
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
├── .gitignore          # Git ignore patterns
├── Procfile            # Heroku process file
└── tests/              # Test suite
    ├── __init__.py
    └── test_bot.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

If you like wisdom-lite and want to support its development, consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs
- 💡 Suggesting new features
- 💰 Supporting via [Venmo](https://venmo.com/code?user_id=2270645291319296805)

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Author

Created by Vikas Sharma
- Website: [vikasvsharma.com](https://vikasvsharma.com)

## Changelog

### Version 2.0 (2026)
- 🔒 Security overhaul: removed hardcoded secrets, added environment configuration
- ⬆️ Upgraded to Python 3.12, Flask 3, SQLAlchemy 2, Twilio 9
- 🗃️ Replaced class-level lists with proper database tables
- 🔐 Added Twilio request signature validation
- 🧪 Added comprehensive pytest test suite
- 📝 Improved documentation and setup instructions
- ♻️ Refactored to use command table pattern
- 🐛 Fixed missing functions and error handling

### Version 1.0 (2020)
- Initial release
