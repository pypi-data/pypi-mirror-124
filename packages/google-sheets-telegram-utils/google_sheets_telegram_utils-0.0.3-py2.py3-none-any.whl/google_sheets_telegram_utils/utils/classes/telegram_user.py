from google_sheets_telegram_utils.exceptions import UserDoesNotExistException, UserAlreadyExistsException
from google_sheets_telegram_utils.utils.sheets_utils import add_row
from google_sheets_telegram_utils.settings import GOOGLE_USERS_SHEET_NAME


class TelegramUser:
    def __init__(self, data):
        #  TODO move id, username... to constants
        self.id = data['id']
        self.username = data['username']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.language_code = data['language_code']
        self.is_bot = data['is_bot']
        self.is_activated = data['is_activated'] and data['is_activated'].lower() == 'true'

    def convert_to_list(self) -> list:
        return [
            self.id,
            self.username,
            self.first_name,
            self.last_name,
            self.language_code,
            self.is_bot,
            'TRUE' if self.is_activated else 'FALSE',
        ]

    def save(self):
        try:
            from google_sheets_telegram_utils.utils.utils import get_user_by_id
            get_user_by_id(self.id)
        except UserDoesNotExistException:
            add_row(self.convert_to_list(), GOOGLE_USERS_SHEET_NAME)
        else:
            raise UserAlreadyExistsException
