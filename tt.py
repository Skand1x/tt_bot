import sqlite3

con = sqlite3.connect('tt.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS work_time_logs
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task_name char(20),
                   user_id INTEGER,
                   start_time TIMESTAMP,
                   end_time TIMESTAMP,
                   duration TIMESTAMP)''')
con.commit()
cur.execute('''CREATE TABLE IF NOT EXISTS relax_time_logs
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task_name char(20),
                   user_id INTEGER,
                   start_time TIMESTAMP,
                   end_time TIMESTAMP,
                   duration TIMESTAMP)''')
con.commit()
cur.execute('''CREATE TABLE IF NOT EXISTS sleep_time_logs
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  task_name char(20),
                   user_id INTEGER,
                   start_time TIMESTAMP,
                   end_time TIMESTAMP,
                   duration TIMESTAMP)''')
con.commit()
