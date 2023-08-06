import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google_sheets_telegram_utils.settings import (
    GOOGLE_SHEETS_CREDENTIALS_PATH,
    GOOGLE_SHEETS_SCOPE,
    GOOGLE_SHEETS_FILE,
)


def get_workbook() -> gspread.models.Spreadsheet:
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        GOOGLE_SHEETS_CREDENTIALS_PATH,
        GOOGLE_SHEETS_SCOPE,
    )
    client = gspread.authorize(credentials)
    sheet = client.open(GOOGLE_SHEETS_FILE)
    return sheet
