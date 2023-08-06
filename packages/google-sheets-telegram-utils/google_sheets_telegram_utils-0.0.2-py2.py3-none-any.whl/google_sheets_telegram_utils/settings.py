import os
import pytz
from os.path import join, dirname
from dotenv import load_dotenv


dotenv_path = join(dirname(__file__), '../../bot_blueprint/src/.env')

# Load file from the path.
load_dotenv(dotenv_path)

TIMEZONE = pytz.timezone('Europe/Minsk')

# Telegram Bot Token
TOKEN = os.getenv('TOKEN')


GOOGLE_SHEETS_CREDENTIALS_PATH = join(dirname(__file__), '../../bot_blueprint/src/client_secret.json')
GOOGLE_SHEETS_SCOPE = ['https://www.googleapis.com/auth/drive']
GOOGLE_SHEETS_FILE = os.getenv('GOOGLE_SHEETS_FILE', 'bot_test_file')
GOOGLE_MAIN_SHEET_NAME = os.getenv('GOOGLE_MAIN_SHEET_NAME', 'main')
GOOGLE_USERS_SHEET_NAME = os.getenv('GOOGLE_USERS_SHEET_NAME', 'users')
