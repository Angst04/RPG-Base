import psycopg2
from core.config import DB_HOST as host, DB_USER as user, DB_PASSWORD as password, DB_NAME as db_name

async def get_ac(callback, ac_name):
   conn = psycopg2.connect(
      host=host,
      user=user,
      password=password,
      database=db_name
   )
   cur = conn.cursor()

   cur.execute(f'SELECT "{ac_name}" FROM achievements WHERE id_tg = %s', [callback.message.chat.id])
   if cur.fetchone() != 1:
      await callback.answer(text=f'Получено достижение!\n\n{ac_name}', show_alert=True)

   cur.execute(f'UPDATE achievements SET "{ac_name}" = 1 WHERE id_tg=%s', [callback.message.chat.id])

   conn.commit()
   cur.close()
   conn.close()