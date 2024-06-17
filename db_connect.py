import time

import gspread
import schedule
from gspread import Client,Spreadsheet,Worksheet
import psycopg2

import params
db_params = params.db_params

SPREADSHEET_URL = params.SPREADSHEET_URL

def main():
    # Подключение к базе данных
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Указываем путь к JSON
    gc = gspread.service_account('./alice-407112-ef9b23917c22.json')
    # Открываем тестовую таблицу
    sh = gc.open_by_url(SPREADSHEET_URL)
    # Выводим значение ячейки A1
    print(sh.sheet1.get('A1'))

    headers = sh.sheet1.row_values(1)

    ls = db_line_count()
    count = ls[0][0]+1

    # Получаем все значения из листа, начиная со второй строки
    values = sh.sheet1.get_all_values()[count:]

    # Проходимся по каждой строке и формируем словарь
    for row in values:
        row_data = dict(zip(headers, row))

        # Формируем SQL-запрос для вставки в базу данных
        query = "INSERT INTO prob (user_name, positions, address) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING"
        cursor.execute(query, (row_data["Restaurant"], row_data["Name"], row_data["Address"]))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    cursor.close()
    conn.close()

def db_line_count():
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM prob")
    ls = cursor.fetchall()

    conn.close()
    return ls




