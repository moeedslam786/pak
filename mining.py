import random
from datetime import datetime, timedelta
from config import MINING_RATE, MINING_COOLDOWN

class MiningSystem:
    @staticmethod
    def can_mine(last_mining):
        if not last_mining:
            return True
        
        last_mining = datetime.strptime(last_mining, '%Y-%m-%d %H:%M:%S.%f')
        time_passed = (datetime.now() - last_mining).total_seconds()
        return time_passed >= MINING_COOLDOWN

    @staticmethod
    def calculate_mining_reward():
        # Base rate with small random variation
        variation = random.uniform(-0.0002, 0.0002)
        return MINING_RATE + variation

    @staticmethod
    def get_cooldown_time(last_mining):
        if not last_mining:
            return 0
        
        last_mining = datetime.strptime(last_mining, '%Y-%m-%d %H:%M:%S.%f')
        time_passed = (datetime.now() - last_mining).total_seconds()
        remaining = MINING_COOLDOWN - time_passed
        return max(0, int(remaining))
