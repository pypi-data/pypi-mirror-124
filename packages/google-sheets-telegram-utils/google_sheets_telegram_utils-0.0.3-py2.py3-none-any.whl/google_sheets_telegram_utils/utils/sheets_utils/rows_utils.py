from google_sheets_telegram_utils.utils.sheets_utils import get_workbook


def add_rows(rows: list, sheet_name) -> None:
    workbook = get_workbook()
    worksheet = workbook.worksheet(sheet_name)
    records = worksheet.get_all_records()
    insert_position = len(records) + 2
    worksheet.insert_rows(rows, insert_position)


def add_row(row, sheet_name):
    return add_rows([row], sheet_name)
