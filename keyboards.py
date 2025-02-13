from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackContext

def get_main_keyboard(language='en'):
    keyboard = [
        [
            InlineKeyboardButton("⚒️ Mine", callback_data='mine'),
            InlineKeyboardButton("💰 Balance", callback_data='balance')
        ],
        [
            InlineKeyboardButton("📋 Tasks", callback_data='tasks'),
            InlineKeyboardButton("🔗 Referral", callback_data='referral')
        ],
        [
            InlineKeyboardButton("⚙️ Settings", callback_data='settings')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_settings_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("🇬🇧 English", callback_data='lang_en'),
            InlineKeyboardButton("🇪🇸 Español", callback_data='lang_es')
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data='main_menu')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_tasks_keyboard():
    keyboard = [
        [
            InlineKeyboardButton("📈 Daily Mining", callback_data='task_daily_mining'),
            InlineKeyboardButton("👥 Invite Friends", callback_data='task_invite')
        ],
        [
            InlineKeyboardButton("🔙 Back", callback_data='main_menu')
        ]
    ]
    return InlineKeyboardMarkup(keyboard)