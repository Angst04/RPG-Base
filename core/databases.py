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
      
      cur.execute('''CREATE TABLE IF NOT EXISTS inventories (
                  id serial PRIMARY KEY,
                  id_tg INTEGER,
                  card_1 TEXT DEFAULT 'c_0001',
                  card_2 TEXT DEFAULT 'c_0002',
                  card_3 TEXT DEFAULT '0',
                  card_4 TEXT DEFAULT '0',
                  card_5 TEXT DEFAULT '0',
                  card_6 TEXT DEFAULT '0',
                  card_7 TEXT DEFAULT '0',
                  card_8 TEXT DEFAULT '0',
                  card_9 TEXT DEFAULT '0'
      )''')
      
      cur.execute('''CREATE TABLE IF NOT EXISTS collections (
                  id serial PRIMARY KEY,
                  id_tg INTEGER,
                  c_0001 INTEGER DEFAULT 1,
                  c_0002 INTEGER DEFAULT 1,
                  c_0003 INTEGER DEFAULT 0,
                  c_0004 INTEGER DEFAULT 0
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
   conn.autocommit = True

   cur.execute(f"DROP TABLE users;")
   cur.execute(f"DROP TABLE users_map;")
   cur.execute(f"DROP TABLE transition_events;")
   cur.execute(f"DROP TABLE achievements;")
   cur.execute(f"DROP TABLE inventories;")
   cur.execute(f"DROP TABLE collections;")

   #conn.commit()
   cur.close()
   conn.close()