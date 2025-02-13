import logging
from datetime import datetime
from functools import wraps
import time

def setup_logging():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

def rate_limit(limit):
    def decorator(func):
        last_time = {}
        
        @wraps(func)
        def wrapper(update, context, *args, **kwargs):
            user_id = update.effective_user.id
            current_time = time.time()
            
            if user_id in last_time:
                time_passed = current_time - last_time[user_id]
                if time_passed < limit:
                    return
            
            last_time[user_id] = current_time
            return func(update, context, *args, **kwargs)
        return wrapper
    return decorator

def format_number(number):
    return f"{number:.8f}"

def get_referral_link(bot_username, user_id):
    return f"https://t.me/{bot_username}?start={user_id}"
