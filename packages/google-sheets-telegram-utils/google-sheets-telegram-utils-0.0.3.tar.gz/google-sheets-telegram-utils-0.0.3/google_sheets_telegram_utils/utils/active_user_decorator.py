from functools import wraps

from google_sheets_telegram_utils.exceptions import UserDoesNotExistException
from google_sheets_telegram_utils.utils.utils import get_user_by_id


def active_user(func):
    @wraps(func)
    def wrapper(update, context):
        pk = update.message.from_user.id
        try:
            user = get_user_by_id(pk=pk)
        except UserDoesNotExistException:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, you are not registered yet",
            )
        else:
            if not user.is_activated:
                context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Sorry, Admin has not activated you yet",
                )
            else:
                return func(update, context)
    return wrapper
