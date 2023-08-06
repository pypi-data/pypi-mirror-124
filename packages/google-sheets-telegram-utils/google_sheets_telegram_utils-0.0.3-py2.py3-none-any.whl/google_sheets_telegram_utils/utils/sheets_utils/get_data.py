from google_sheets_telegram_utils.utils.sheets_utils import get_workbook


def get_data_from_sheet(sheet_name: str) -> dict:
    workbook = get_workbook()
    sheet = workbook.worksheet(sheet_name)
    data = sheet.get_all_records()
    return data
