import psycopg2
from database_config import host, user, password, db_name

try:
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute('SELECT version();')
   print(f'Текущая версия {cur.fetchone()}')

except Exception as e:
   print('[CATH ERROR]', e)
finally:
   if conn:
      cur.close()
      conn.close()
      print('[INFO] Соединение с БД закрыто')