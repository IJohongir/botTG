import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
admins = [
    557371080
]

ip = os.getenv("ip")

redis = {
    'address': (ip, 6379),
    'encoding': 'utf8'
}
