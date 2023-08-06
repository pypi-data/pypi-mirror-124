from google_sheets_telegram_utils.exceptions import UserDoesNotExistException
from google_sheets_telegram_utils.utils.classes.telegram_user import TelegramUser
from google_sheets_telegram_utils.settings import GOOGLE_USERS_SHEET_NAME
from google_sheets_telegram_utils.utils.sheets_utils import get_data_from_sheet


def get_user_by_id(pk) -> TelegramUser:
    users = get_data_from_sheet(GOOGLE_USERS_SHEET_NAME)
    filtered_users = list(filter(lambda user: user['id'] == pk, users))
    if filtered_users:
        user_data = filtered_users[0]
        telegram_user = TelegramUser(user_data)
        return telegram_user
    raise UserDoesNotExistException
