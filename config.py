import os

# Bot Configuration
BOT_TOKEN = "YOUR_BOT_TOKEN"  # Replace with actual token

# Database Configuration
DATABASE_NAME = "crypto_mining_bot.db"

# Mining Configuration
MINING_RATE = 0.001  # Base mining rate per minute
MINING_COOLDOWN = 300  # 5 minutes cooldown between mining sessions

# Referral Configuration
REFERRAL_BONUS = 0.01  # Bonus for referrer
REFERRAL_REWARD = 0.005  # Bonus for new user

# Task Configuration
DAILY_TASK_REWARD = 0.005
TASKS_COOLDOWN = 86400  # 24 hours in seconds

# Rate Limiting
RATE_LIMIT = 1  # Requests per second
