import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

async def busy_change(chat_id, status):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   if status:
      cur.execute(f'UPDATE users SET busy = 1 WHERE id_tg=%s', [chat_id])
   else:
      cur.execute(f'UPDATE users SET busy = 0 WHERE id_tg=%s', [chat_id])
   conn.commit()
   cur.close()
   conn.close()
   
async def busy_check(message):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()
   cur.execute(f'SELECT busy FROM users WHERE id_tg=%s', [message.chat.id])
   res = cur.fetchone()[0]
   cur.close()
   conn.close()
   if res == 1:
      return True
   return False