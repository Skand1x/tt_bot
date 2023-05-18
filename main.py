import os
import dotenv
import telebot
import datetime
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv, find_dotenv
from telebot import types
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

con = sqlite3.connect('tt.db', check_same_thread=False)
cur = con.cursor()
db_connection = sqlite3.connect('tt.db')

load_dotenv(find_dotenv())

 
bot = telebot.TeleBot(os.getenv('TG_KEY'))

@bot.message_handler(commands=['start'])
def welcome(message):
        sticker = open('E:/TimeTracker-by-Klim/Welcome.webp', 'rb')
        bot.send_sticker(message.chat.id, sticker)

        # гл кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Item1 = types.KeyboardButton("👨‍💻Работа")
        Item2 = types.KeyboardButton("🥹Отдых")
        Item3 = types.KeyboardButton("😴Сон")
        Item4 = types.KeyboardButton("Показать аналитику")

        markup.add(Item1, Item2, Item3, Item4)

        bot.send_message(message.chat.id, "Приветствую тебя, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помочь пользователям управлять своим временем. Я отслеживаю потраченное время на работу, отдых и сон, и могу вывести аналитику потраченного времени.".format(message.from_user, bot.get_me()),
            parse_mode='html', reply_markup=markup)
# инлайн кнопки
@bot.message_handler(content_types=['text'])
def callback_inline(message):
        if message.chat.type == 'private':
                if message.text == '👨‍💻Работа':
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        Item5 = types.InlineKeyboardButton("Начать работать :(", callback_data='start_work')
                        Item6 = types.InlineKeyboardButton("Закончить работать :)", callback_data='end_work')

                        markup.add(Item5, Item6)

                        bot.send_message(message.chat.id, 'Выбирай:', reply_markup=markup)


                elif message.text == '🥹Отдых':
                
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        Item7 = types.InlineKeyboardButton("Начать Отдыхать :)", callback_data='start_relax')
                        Item8 = types.InlineKeyboardButton("Закончить Отдыхать :(", callback_data='end_relax')

                        markup.add(Item7, Item8)

                        bot.send_message(message.chat.id, 'Выбирай:', reply_markup=markup)

                
                elif message.text == '😴Сон':
                
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        Item9 = types.InlineKeyboardButton("Начать Сон :)", callback_data='start_sleep')
                        Item10 = types.InlineKeyboardButton("Закончить Сон :(", callback_data='end_sleep')

                        markup.add(Item9, Item10)

                        bot.send_message(message.chat.id, 'Выбирай:', reply_markup=markup)
                
                elif message.text == 'Показать аналитику':
                
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        Item11 = types.InlineKeyboardButton("➡️Показать аналитику", callback_data='show_analytics')
                        Item12 = types.InlineKeyboardButton("пока пустышка", callback_data='lol')

                        markup.add(Item11, Item12)

                        bot.send_message(message.chat.id, 'Выбирай:', reply_markup=markup)
                
# Код для заноса в бд
@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
        chat_id = call.message.chat.id
        user_id = call.message.from_user.id
        # Работа
        if call.data == 'start_work':

                # Запись времени начала работы в базу данных
                start_time = datetime.datetime.now()
                task_name = 'Работа'  # Можно добавить возможность ввода названия задачи
                
                cur.execute("INSERT INTO work_time_logs (task_name, start_time, user_id) VALUES (?, ?, ?)", (task_name, start_time, user_id))
                con.commit()
                
                bot.send_message(chat_id, "Вы начали работать. Чтобы закончить, нажмите кнопку 'Закончить работать :)'.")

        elif call.data == 'end_work':

                # Получение последней записи в базе данных для этого пользователя
                cur.execute("SELECT * FROM work_time_logs WHERE user_id = ? AND end_time IS NULL", (user_id,))
                last_record = cur.fetchone()
                if last_record is None:
                        bot.send_message(chat_id, "Ошибка: нет активной задачи.")
                        return

                # Запись времени окончания работы в базу данных
                end_time = datetime.datetime.now()

                # Рассчитываем продолжительность работы
                duration_seconds = int((end_time - datetime.datetime.strptime(last_record[3], '%Y-%m-%d %H:%M:%S.%f')).total_seconds())
                hours, remainder = divmod(duration_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration = f"{hours:02}:{minutes:02}:{seconds:02}"

                # Обновление записи в базе данных с временем окончания работы и продолжительностью
                cur.execute("UPDATE work_time_logs SET end_time=?, duration=? WHERE id=?", (end_time, duration, last_record[0]))
                con.commit()
                
                bot.send_message(chat_id, f"Работа завершена. Время работы: {duration}")

        # Отдых
        if call.data == 'start_relax':

                # Запись времени начала работы в базу данных
                start_time = datetime.datetime.now()
                task_name = 'Отдых'  # Можно добавить возможность ввода названия задачи
                
                cur.execute("INSERT INTO relax_time_logs (task_name, start_time, user_id) VALUES (?, ?, ?)", (task_name, start_time, user_id))
                con.commit()
                
                bot.send_message(chat_id, "Отдых начался. Чтобы закончить, нажмите кнопку 'Закончить Отдыхать :('.")

        elif call.data == 'end_relax':

                # Получение последней записи в базе данных для этого пользователя
                cur.execute("SELECT * FROM relax_time_logs WHERE user_id = ? AND end_time IS NULL", (user_id,))
                last_record = cur.fetchone()
                if last_record is None:
                        bot.send_message(chat_id, "Ошибка: нет активной задачи.")
                        return

                # Запись времени окончания работы в базу данных
                end_time = datetime.datetime.now()
                
                # Рассчитываем продолжительность работы
                duration_seconds = int((end_time - datetime.datetime.strptime(last_record[3], '%Y-%m-%d %H:%M:%S.%f')).total_seconds())
                hours, remainder = divmod(duration_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration = f"{hours:02}:{minutes:02}:{seconds:02}"
                
                # Обновление записи в базе данных с временем окончания работы и продолжительностью
                cur.execute("UPDATE relax_time_logs SET end_time=?, duration=? WHERE id=?", (end_time, duration, last_record[0]))
                con.commit()
                
                bot.send_message(chat_id, f"Отдых завершен. Время отдыха: {duration} секунд.")

        # Сон
        if call.data == 'start_sleep':

                # Запись времени начала сна в базу данных
                start_time = datetime.datetime.now()
                task_name = 'Сон'  # Можно добавить возможность ввода названия задачи
                
                cur.execute("INSERT INTO sleep_time_logs (task_name, start_time, user_id) VALUES (?, ?, ?)", (task_name, start_time, user_id))
                con.commit()
                
                bot.send_message(chat_id, "Спокойной ночи. Когда проснетесь, нажмите кнопку 'Закончить Сон :('.")

        elif call.data == 'end_sleep':

                # Получение последней записи в базе данных для этого пользователя
                cur.execute("SELECT * FROM sleep_time_logs WHERE user_id = ? AND end_time IS NULL", (user_id,))
                last_record = cur.fetchone()
                if last_record is None:
                        bot.send_message(chat_id, "Ошибка: нет активной задачи.")
                        return

                # Запись времени окончания работы в базу данных
                end_time = datetime.datetime.now()
                
                # Рассчитываем продолжительность работы
                duration_seconds = int((end_time - datetime.datetime.strptime(last_record[3], '%Y-%m-%d %H:%M:%S.%f')).total_seconds())
                hours, remainder = divmod(duration_seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration = f"{hours:02}:{minutes:02}:{seconds:02}"
                
                # Обновление записи в базе данных с временем окончания сна и продолжительностью
                cur.execute("UPDATE sleep_time_logs SET end_time=?, duration=? WHERE id=?", (end_time, duration, last_record[0]))
                con.commit()
                
                bot.send_message(chat_id, f"Сон завершен. Время сна: {duration} секунд.")

# закрыть бд
#con.close()


# АНАЛИТИКА потраченного времени
'''
# Обработчик нажатия кнопки "Показать аналитику"
@bot.callback_query_handler(func=lambda call: call.data == 'show_analytics')
def show_analytics_handler(call):
    user_id = call.from_user.id

    # Получение аналитики времени пользователя
    analytics = get_user_analytics(user_id)

    # Создание графика аналитики времени
    create_time_chart(analytics, user_id)

def get_user_analytics(user_id):
    # Запрос аналитики времени из трех таблиц
    query = """
    SELECT task_name, SUM(duration) AS total_duration
    FROM (
        SELECT 'work' AS task_name, duration FROM work_time_logs WHERE user_id=?
        UNION ALL
        SELECT 'relax' AS task_name, duration FROM relax_time_logs WHERE user_id=?
        UNION ALL
        SELECT 'sleep' AS task_name, duration FROM sleep_time_logs WHERE user_id=?
    )
    GROUP BY task_name
    """
    df = pd.read_sql_query(query, db_connection, params=(user_id, user_id, user_id))

    # Преобразование данных в формат datetime
    df['duration'] = pd.to_timedelta(df['duration'])

    # Группировка данных по типу задачи и вычисление общего времени для каждого типа
    analytics = df.groupby('task_name').sum()

    # Форматирование времени в формат чч:мм:сс
    analytics['duration'] = analytics['duration'].dt.total_seconds().apply(lambda x: '{:02d}:{:02d}:{:02d}'.format(*divmod(int(x), 60**2, 60)))
    
    return analytics

# Функция для построения графика аналитики времени
def create_time_chart(analytics, user_id):
    # Создание графика
    fig, ax = plt.subplots()

    # Построение столбчатой диаграммы
    ax.bar(analytics.index, analytics['duration'])

    # Добавление подписей осей
    ax.set_xlabel('Task Type')
    ax.set_ylabel('Total Duration')

    # Добавление заголовка графика
    ax.set_title('Time Analytics')

    # Сохранение графика в файл
    chart_filename = f'time_analytics_{user_id}.png'
    fig.savefig(chart_filename)

    # Отправка графика пользователю
    bot.send_photo(chat_id=user_id, photo=open(chart_filename, 'rb'))

    # Удаление временного файла с графиком
    os.remove(chart_filename)
'''

@bot.callback_query_handler(func=lambda call: call.data == 'show_analytics')
def show_analytics_handler(call):
    user_id = call.from_user.id

    # Получение аналитики времени пользователя
    analytics = get_user_analytics(user_id)

    # Создание графика аналитики времени
    create_time_chart(analytics, user_id)

def get_user_analytics(user_id):
    # Загрузка данных из таблицы работы
    work_data = pd.read_sql_query(f"SELECT duration FROM work_time_logs WHERE user_id={user_id}", db_connection)
    work_duration = sum(work_data['duration'].apply(parse_duration).astype(int))

    # Загрузка данных из таблицы отдыха
    relax_data = pd.read_sql_query(f"SELECT duration FROM relax_time_logs WHERE user_id={user_id}", db_connection)
    relax_duration = sum(relax_data['duration'].apply(parse_duration).astype(int))

    # Загрузка данных из таблицы сна
    sleep_data = pd.read_sql_query(f"SELECT duration FROM sleep_time_logs WHERE user_id={user_id}", db_connection)
    sleep_duration = sum(sleep_data['duration'].apply(parse_duration).astype(int))

  # Создание DataFrame для аналитики
    df = pd.DataFrame({
        'Task Type': ['Work', 'Relax', 'Sleep'],
        'Total Duration': [work_duration, relax_duration, sleep_duration]
    })

    # Форматирование продолжительности в формат часы:минуты:секунды
    df['Formatted Duration'] = df['Total Duration'].apply(format_duration)

    return df

def parse_duration(duration):
    parts = duration.split(':')
    hours = int(parts[0])
    minutes = int(parts[1])
    seconds = int(parts[2])
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds

def format_duration(duration):
    hours = duration // 3600
    minutes = (duration % 3600) // 60
    seconds = duration % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def create_time_chart(analytics, user_id):
    # Создание графика
    fig, ax = plt.subplots()

    # Построение столбчатой диаграммы
    ax.bar(analytics['Task Type'], analytics['Total Duration'])

    # Добавление подписей осей
    ax.set_xlabel('Task Type')
    ax.set_ylabel('Total Duration')

    # Добавление заголовка графика
    ax.set_title('Time Analytics')

    # Сохранение графика в файл
    chart_filename = f'time_analytics_{user_id}.png'
    fig.savefig(chart_filename)

    # Отправка графика пользователю
    with open(chart_filename, 'rb') as photo:
        bot.send_photo(chat_id=user_id, photo=photo)

    # Удаление временного файла с графиком
        os.remove(chart_filename)

#RUN
bot.polling()