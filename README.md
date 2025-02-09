# Shakespr - AI-Empowered Life Path Simulator Bot

Shakespr is a Telegram bot designed to help users simulate life decisions, particularly focusing on city relocation. The bot integrates real-time data from Numbeo to provide accurate cost of living comparisons and insights.

## Features

- 🏢 **User Profile Management**: Create and maintain personal profiles
- 🌎 **City Relocation Simulation**: Compare cost of living between cities
- 💰 **Real-time Data**: Integration with Numbeo for up-to-date cost information
- 📊 **Local Data Storage**: PostgreSQL database for efficient data management
- 🔄 **Automatic Updates**: Daily data refresh for accuracy

## Project Structureshakespr/
```
├── alembic/                      # Database migrations
├── config/                       # Configuration files
│   ├── database.env             # Database credentials
│   └── bot.env                  # Bot token and settings
├── data/                        # Data storage
│   └── logs/                    # Log files
├── sql/                         # SQL scripts
│   ├── numbeo_data/             # Numbeo database schema
│   │   ├── schema/
│   │   └── procedures/
│   └── user_data/              # User database schema
│       ├── schema/
│       └── procedures/
├── src/                        # Source code
│   ├── bot/                   # Bot-specific code
│   │   └── handlers/         # Command handlers
│   ├── data/                 # Data management
│   │   └── numbeo/          # Numbeo data handling
│   └── utils/               # Utility functions
├── tests/                    # Test files
├── requirements.txt          # Python dependencies
└── README.md                # Project documentation
```

## Database Structure

### User Database (user_data)
- **Schema**: bot
- **Tables**:
  - user_profiles: User information
  - simulations: Simulation history

### Numbeo Database (numbeo_data)
- **Schema**: numbeo_col
- **Tables**:
  - cities: City information
  - updates: Data update tracking
  - Various cost_sets tables (restaurant, market, etc.)

## Setup Instructions

1. **Prerequisites**:
```bash
# Install PostgreSQL
sudo apt update
sudo apt install postgresql postgresql-contrib

# Install Python requirements
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
2. Database Setup:
# Connect as postgres superuser
sudo -u postgres psql

# Create databases and users
CREATE DATABASE numbeo_data;
CREATE DATABASE user_data;
CREATE USER numbeo_admin WITH PASSWORD '1234';
CREATE USER bot_admin WITH PASSWORD '1234';

# Grant privileges
GRANT CONNECT ON DATABASE numbeo_data TO numbeo_admin;
GRANT CONNECT ON DATABASE user_data TO bot_admin;

# Connect to each database and set up schemas
\c numbeo_data
CREATE SCHEMA numbeo_col;
GRANT ALL PRIVILEGES ON SCHEMA numbeo_col TO numbeo_admin;

\c user_data
CREATE SCHEMA bot;
GRANT ALL PRIVILEGES ON SCHEMA bot TO bot_admin;

# Exit PostgreSQL
\q

# Run schema initialization scripts
psql -h localhost -p 5432 -U numbeo_admin -d numbeo_data -f sql/numbeo_data/schema/init.sql
psql -h localhost -p 5432 -U bot_admin -d user_data -f sql/user_data/schema/init.sql
3. Environment Setup:
# Copy example env file
cp config/.env.example config/.env

# Edit with your credentials
nano config/.env
4. Bot Setup:
- Create a new bot with [@BotFather](https://t.me/botfather) on Telegram
- Copy the token to your .env file

5. Running the Bot:
python run_bot.py
## Available Commands

- /start - Initialize the bot
- /profile - Create or update your profile
- /relocate - Start a city relocation simulation
- /help - Show available commands

## Development

1. Creating New Handlers:
- Add new handler files in src/bot/handlers/
- Register handlers in src/main.py

2. Database Migrations:
- Use Alembic for schema changes
- Create new migrations: alembic revision -m "description"
- Apply migrations: alembic upgrade head

## Deployment

The project is designed to be deployed on cloud platforms:

1. Heroku:
- Uses Procfile for process management
- Automatic database migrations on release
- Environment variables for configuration
