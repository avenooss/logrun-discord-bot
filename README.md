# LogRun - Enterprise-Grade Discord Guild Management Bot

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/discord.py-2.x-blue.svg)](https://github.com/Rapptz/discord.py)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](Dockerfile)

A production-grade Discord bot designed for World of Warcraft guilds, providing automatic player verification through Warcraft Logs and Battle.net APIs, intelligent role assignment, guild statistics, and comprehensive guild management capabilities.

## 🎯 Features

### Core Functionality
- **Automatic Verification System**: Verify players using Warcraft Logs and Battle.net credentials
- **Intelligent Role Assignment**: Automatic role distribution based on Heroic Best Performance Average
- **Guild Roster Management**: Track and manage guild members with detailed profiles
- **Performance Leaderboards**: Real-time leaderboards sorted by player performance
- **Guild Statistics**: Comprehensive guild-wide statistics and analytics
- **Automated Refresh**: Scheduled background tasks to keep player data current

### Discord Integration
- **Slash Commands**: Modern command interface
- **Context Menu Commands**: Right-click command actions
- **Interactive Buttons & Modals**: User-friendly data input and confirmation
- **Dropdown Menus**: Streamlined selection interfaces
- **Rich Embeds**: Professional, formatted responses
- **Pagination**: Handle large datasets efficiently
- **Persistent Views**: Maintain button/menu state across bot restarts

### Admin Features
- **Server Setup Wizard**: Automated Discord server structure creation
- **Permission Management**: Granular permission controls
- **Audit Logging**: Track all administrative actions
- **Data Export/Import**: Backup and restore guild data
- **Health Monitoring**: Monitor bot and API health

### Security
- **Environment Variable Configuration**: Secure credential management
- **Permission Hierarchy Validation**: Enforce Discord role permissions
- **Rate Limiting**: Respect API rate limits
- **Input Validation**: Sanitize all user inputs
- **Error Handling**: Graceful failure recovery

## 📋 Prerequisites

- Python 3.12+
- Discord.py 2.x
- PostgreSQL or SQLite
- Docker & Docker Compose (optional)
- Warcraft Logs API key (Client ID + Client Secret)
- Battle.net API key
- Discord Bot Token

## 🚀 Quick Start

### Local Development

```bash
# Clone the repository
git clone https://github.com/avenooss/logrun-discord-bot.git
cd logrun-discord-bot

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Configure your .env file with API keys and tokens
nano .env

# Run the bot
python -m src.main
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f bot

# Stop the bot
docker-compose down
```

## 🔧 Configuration

All configuration is managed through `.env` file:

```env
# Discord
DISCORD_TOKEN=your_discord_bot_token

# Warcraft Logs
WARCRAFT_LOGS_CLIENT_ID=your_client_id
WARCRAFT_LOGS_CLIENT_SECRET=your_client_secret

# Battle.net
BATTLENET_API_KEY=your_api_key
BATTLENET_REGION=us  # us, eu, kr, tw, cn

# Database
DATABASE_URL=sqlite:///./logrun.db
# Or for PostgreSQL: DATABASE_URL=postgresql://user:password@localhost/logrun

# Bot Settings
LOG_LEVEL=INFO
REFRESH_INTERVAL=3600
CACHE_TTL=1800
```

## 📁 Project Structure

```
logrun-discord-bot/
├── src/
│   ├── main.py                 # Entry point
│   ├── config/
│   │   ├── settings.py         # Configuration management
│   │   ├── constants.py        # Application constants
│   │   └── logging_config.py   # Logging setup
│   ├── bot/
│   │   ├── bot.py              # Bot initialization
│   │   ├── cogs/
│   │   │   ├── __init__.py
│   │   │   ├── setup.py        # Server setup commands
│   │   │   ├── verification.py # Verification system
│   │   │   ├── guild.py        # Guild management
│   │   │   ├── admin.py        # Admin commands
│   │   │   └── info.py         # Information commands
│   │   ├── commands/
│   │   │   ├── __init__.py
│   │   │   ├── slash_commands.py
│   │   │   └── context_menu.py
│   │   ├── views/
│   │   │   ├── __init__.py
│   │   │   ├── buttons.py
│   │   │   ├── modals.py
│   │   │   ├── select_menus.py
│   │   │   └── pagination.py
│   │   └── embeds/
│   │       ├── __init__.py
│   │       ├── verification.py
│   │       ├── profiles.py
│   │       ├── leaderboards.py
│   │       └── statistics.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── warcraft_logs.py    # Warcraft Logs API client
│   │   ├── battle_net.py       # Battle.net API client
│   │   ├── verification.py     # Verification logic
│   │   ├── role_manager.py     # Role assignment logic
│   │   ├── guild_manager.py    # Guild management
│   │   ├── cache.py            # Caching layer
│   │   └── scheduler.py        # Background tasks
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── connection.py       # Database initialization
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── character.py
│   │   │   ├── guild.py
│   │   │   └── statistics.py
│   │   └── migrations/
│   │       └── alembic/
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py           # Logging utilities
│   │   ├── decorators.py       # Custom decorators
│   │   ├── validators.py       # Input validation
│   │   ├── errors.py           # Custom exceptions
│   │   └── helpers.py          # Helper functions
│   └── api/
│       ├── __init__.py
│       └── health.py           # Health check endpoint (Flask)
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_services.py
│   │   ├── test_validators.py
│   │   └── test_repositories.py
│   ├── integration/
│   │   └── test_bot.py
│   └── fixtures/
│       └── sample_data.py
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
├── .github/
│   └── workflows/
│       ├── lint.yml
│       ├── test.yml
│       └── deploy.yml
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
├── Makefile
└── LICENSE
```

## 🎮 Discord Server Structure

### Categories
- **Information**: Server announcements and guides
- **General**: General discussion channels
- **Raid**: Raid-specific channels
- **Logs**: Warcraft Logs integration
- **Administration**: Officer and admin channels
- **Utilities**: Bot-specific channels

### Channels
- `#let-start`: Welcome and getting started
- `#bot-guide`: Bot usage guide
- `#announcements`: Guild announcements
- `#general`: General chat
- `#raid-chat`: Raid discussion
- `#raid-signup`: Raid event signups
- `#logs`: Raid logs and analysis
- `#bot-logs`: Bot activity logs
- `#officers`: Officer-only channel

## 👥 Role Structure

### Rank Roles
Based on Warcraft Logs Heroic Best Performance Average:

| Performance Range | Role           |
|------------------|----------------|
| 0-24             | Member         |
| 25-49            | Casual Player  |
| 50-74            | Casual Raider  |
| 75-94            | Raider+        |
| 95-98            | Raider++       |
| 99               | Raider Elite   |
| 100              | GOD            |

### Class Roles
Warrior, Paladin, Hunter, Rogue, Priest, Death Knight, Shaman, Mage, Warlock, Monk, Druid, Demon Hunter, Evoker

### Role Types
Tank, Healer, DPS

### Administration
Guild Master, Officer, Raid Leader, Bot Manager

## 📊 Commands

### User Commands
- `/verify` - Link your Battle.net account and verify your character
- `/mylog` - View your latest Warcraft Logs performance
- `/profile` - View your guild member profile
- `/refresh` - Manually refresh your performance data
- `/leaderboard` - View guild-wide leaderboards
- `/stats` - View guild statistics
- `/class` - View class-specific statistics
- `/help` - Display help information

### Admin Commands
- `/setup` - Initialize server with categories, channels, and roles
- `/admin` - Access admin panel
- `/delete_all` - Delete all bot-created structures
- `/export` - Export guild data
- `/import` - Import guild data

## 🔄 API Integrations

### Warcraft Logs
- OAuth2 Client Credentials flow
- GraphQL API for character performance data
- Automatic token refresh
- Rate limit handling
- Heroic Best Performance Average tracking

### Battle.net
- REST API for character verification
- Character profile validation
- Realm and region support

## 📅 Automated Tasks

- **Hourly**: Refresh player performance data
- **Daily**: Guild statistics update
- **Weekly**: Leaderboard refresh and cleanup
- **Daily**: Database backup

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_services.py

# Run in watch mode
pytest-watch
```

## 📝 Code Quality

```bash
# Format code with Black
black src tests

# Sort imports with isort
isort src tests

# Type checking with mypy
mypy src

# Lint with flake8
flake8 src tests
```

## 🐳 Docker

### Build
```bash
docker build -t logrun-bot:latest .
```

### Run
```bash
docker run -d \
  --name logrun \
  --env-file .env \
  -v logrun_data:/app/data \
  logrun-bot:latest
```

### Docker Compose
```bash
docker-compose up -d
docker-compose logs -f
docker-compose down
```

## 📊 Architecture

### Clean Architecture Layers

1. **Presentation Layer**: Discord commands, views, embeds
2. **Application Layer**: Cogs, command handlers
3. **Domain Layer**: Business logic (verification, role assignment)
4. **Infrastructure Layer**: API clients, database, cache
5. **Cross-Cutting Concerns**: Logging, error handling, validation

### Data Flow

```
User Command
    ↓
Command Handler
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Database / External APIs
    ↓
Response → Discord Embed/Message
```

## 🔒 Security Considerations

- All secrets stored in environment variables
- No credentials in source code
- Permission validation on all commands
- Input sanitization and validation
- Rate limit compliance
- Graceful error handling without exposing internals

## 📈 Performance

- In-memory caching with TTL
- Database connection pooling
- Async/await throughout
- Batch operations where possible
- Efficient database queries with indexes

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes following PEP 8 and project structure
4. Write tests for new functionality
5. Run linting and tests
6. Commit with clear messages
7. Push to the branch
8. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For issues, questions, or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- discord.py community
- Warcraft Logs API documentation
- Battle.net API documentation
- Python async/await patterns

---

**LogRun** - Intelligent World of Warcraft Guild Management for Discord
