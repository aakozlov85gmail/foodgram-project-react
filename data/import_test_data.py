# Для загрузки данных в файле csv были предварительно изменены разделители ;
# а также " заменены на '

import os
import csv
import sqlite3


CURRENT_DIR = os.path.dirname(__file__)
DATABASE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, '..', 'backend'))
# База данных
DATABASE = os.path.join(DATABASE_DIR, 'db.sqlite3')
# Файлы с данными
INGREGIENTS = os.path.join(CURRENT_DIR, 'ingredients.csv')

dbtables = {
    INGREGIENTS: 'recipes_ingredient',
}

# Подключение к БД
con = sqlite3.connect(DATABASE)
cur = con.cursor()

try:
    for staticfile in dbtables:
        with open(staticfile, 'r', newline='\n', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                sqlquery = f'INSERT INTO {dbtables[staticfile]} (name, measurement_unit) VALUES ("{row[0]}", "{row[1]}")'
                cur.execute(sqlquery)
    print('Ура! Данные успешно загружены!')
except Exception as error:
    print(f'Ошибка загрузки данных! {error}')
con.commit()
con.close()
