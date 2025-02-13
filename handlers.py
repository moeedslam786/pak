from telegram import Update
from telegram.ext import ContextTypes
from config import REFERRAL_BONUS, REFERRAL_REWARD
from keyboards import get_main_keyboard, get_settings_keyboard, get_tasks_keyboard
from mining import MiningSystem
from utils import rate_limit, format_number, get_referral_link
import logging

class BotHandlers:
    def __init__(self, db):
        self.db = db

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        message = update.message

        # Handle referral
        if len(context.args) > 0:
            try:
                referrer_id = int(context.args[0])
                if referrer_id != user.id:  # Prevent self-referral
                    self.db.add_user(user.id, user.username, referrer_id)
                    # Give bonus to referrer
                    self.db.update_balance(referrer_id, REFERRAL_BONUS)
                    # Give bonus to new user
                    self.db.update_balance(user.id, REFERRAL_REWARD)
            except ValueError:
                logging.warning(f"Invalid referral parameter: {context.args[0]}")
        else:
            self.db.add_user(user.id, user.username)

        await message.reply_text(
            "Welcome to Crypto Mining Simulator!",
            reply_markup=get_main_keyboard()
        )

    @rate_limit(1)
    async def mine(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id

        user_data = self.db.get_user(user_id)
        if not user_data:
            await query.edit_message_text("Please start the bot first!")
            return

        if not MiningSystem.can_mine(user_data[6]):  # last_mining is at index 6
            cooldown = MiningSystem.get_cooldown_time(user_data[6])
            await query.edit_message_text(f"Please wait {cooldown} seconds!")
            return

        reward = MiningSystem.calculate_mining_reward()
        self.db.update_balance(user_id, reward)
        self.db.update_last_mining(user_id)

        await query.edit_message_text(
            f"Mining successful!\nEarned: {format_number(reward)} BTC",
            reply_markup=get_main_keyboard()
        )

    async def balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id

        user_data = self.db.get_user(user_id)
        if not user_data:
            await query.edit_message_text("Please start the bot first!")
            return

        balance = user_data[2]  # balance is at index 2
        await query.edit_message_text(
            f"Your current balance: {format_number(balance)} BTC",
            reply_markup=get_main_keyboard()
        )

    async def settings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            "⚙️ Settings\nChoose your language:",
            reply_markup=get_settings_keyboard()
        )

    async def tasks(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            "📋 Daily Tasks:",
            reply_markup=get_tasks_keyboard()
        )

    async def referral(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id

        referral_link = get_referral_link(context.bot.username, user_id)
        await query.edit_message_text(
            f"🔗 Your referral link:\n{referral_link}\n\n"
            f"Share this link with your friends and earn {REFERRAL_BONUS} BTC for each referral!",
            reply_markup=get_main_keyboard()
        )