import psycopg2
from core.dbs_config import host, user, password, db_name

def firstSeen(get_id, name):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   cur.execute(f'SELECT id_tg FROM "{name}" WHERE id_tg=%s', (get_id,))
   rez = cur.fetchall()

   if not rez:
      addUser(get_id, name, conn, cur)
      return True
   else:
      return False


def addUser(user_id, name, conn, cur):
   cur.execute(f'INSERT INTO "{name}" (id_tg) VALUES (%s)', (user_id,))
   conn.commit()
   cur.close()
   conn.close()

def start():
   try:
      conn = psycopg2.connect(
         host=host,
         user=user,
         password=password,
         database=db_name
      )
      conn.autocommit = True
      cur = conn.cursor()

      cur.execute('''CREATE TABLE IF NOT EXISTS users (
                  id serial PRIMARY KEY,
                  id_tg INTEGER,
                  speed INTEGER DEFAULT 5
      )''')

      cur.execute('''CREATE TABLE IF NOT EXISTS users_map (
                  id serial PRIMARY KEY,
                  id_tg INTEGER,
                  now_location TEXT DEFAULT 'Эвертон',
                  Copper INTEGER DEFAULT 0,
                  Emberwood INTEGER DEFAULT 0
                  )''')

      cur.execute('''CREATE TABLE IF NOT EXISTS transition_events (
                  id serial PRIMARY KEY,
                  id_tg INTEGER,
                  last_event INTEGER DEFAULT 0,
                  Западня INTEGER DEFAULT 0,
                  Чертополох INTEGER DEFAULT 0
                  )''')

      cur.execute('''CREATE TABLE IF NOT EXISTS achievements (
                  id serial PRIMARY KEY,
                  id_tg INTEGER,
                  a1 INTEGER DEFAULT 0,
                  a2 INTEGER DEFAULT 0
                  )''')

   except Exception as e:
      print('[CATCH ERROR]', type(e).__name__, e)

   finally:
      if conn:
         cur.close()
         conn.close()
         print('[INFO] Соединение с БД закрыто')

def drop():
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   cur.execute(f"DROP TABLE users;")
   cur.execute(f"DROP TABLE users_map;")
   cur.execute(f"DROP TABLE transition_events;")
   cur.execute(f"DROP TABLE achievements;")

   conn.commit()
   cur.close()
   conn.close()