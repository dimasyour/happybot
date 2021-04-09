import sqlite3
import matplotlib.pyplot as plt
import uuid

import numpy as np

conn = sqlite3.connect("base.db", check_same_thread=False)
cursor = conn.cursor()


# добавляет нового пользователя с его данными
def register_new_user(user_id):
    rowString = (int(user_id), '1')
    cursor.execute("INSERT INTO user (user_id, user_result) VALUES (?,?)", rowString)
    conn.commit()


# сохраняет результат тест с датой и временем
def result_insert_db(user_id, test_id, test_result, date_result):
    rowString = (
        int(user_id), int(test_id), int(test_result), int(date_result.date().year), int(date_result.date().month),
        int(date_result.date().day), int(date_result.time().hour), int(date_result.time().minute))
    cursor.execute(
        "INSERT INTO user_result (user_id, test_id, test_result, dt_year, dt_month, dt_day, dt_hour, dt_minute) VALUES (?,?,?,?,?,?,?,?)",
        rowString)
    conn.commit()


# создает график и возвращает путь до файла с ним
def result_to_graph(user_id, test_id):
    cursor.execute("SELECT * FROM user_result WHERE user_id = %d AND test_id = %d" % (user_id, test_id))
    records = cursor.fetchall()
    resultAll = []
    for x in records:
        resultAll.append(int(x[2]))
    color_rectangle = np.random.rand(7, 3)
    labels = []
    for i in range(1, len(resultAll) + 1):
        labels.append('Т-' + str(i))
    x = np.arange(len(labels))
    plt.bar(range(len(resultAll)), resultAll, color=color_rectangle)
    plt.title('Результаты оценки вашего Индекса Счастья')
    plt.xticks(x, labels)
    plt.xlabel('Ваши измерения', fontweight='bold', fontsize=10)
    if test_id == 1:
        plt.ylabel('Баллов по Шкале Э.Динера', fontweight='bold', fontsize=12)
    elif test_id == 2:
        plt.ylabel('Баллов по Шкале С.Любомирски', fontweight='bold', fontsize=12)
    pathGraph = 'res/graph/' + str(uuid.uuid4())
    plt.savefig(pathGraph)
    plt.clf()
    return pathGraph+'.png'
