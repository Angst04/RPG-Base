import psycopg2
from core.dbs_config import host, user, password, db_name

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