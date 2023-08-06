from google_sheets_telegram_utils.exceptions import UserAlreadyExistsException
from google_sheets_telegram_utils.utils.classes.telegram_user import TelegramUser


def register_handler(update, context):
    telegram_user = TelegramUser(update.message.from_user)
    try:
        telegram_user.save()
    except UserAlreadyExistsException:
        update.message.reply_text('You are already registered.')
    except Exception as err:  # TODO use more specific exception
        update.message.reply_text('Cannot register now :c')
    else:
        update.message.reply_text('You have been registered. Admin will activate you soon, maybe :3')
