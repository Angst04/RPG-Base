from random import random, choice
import sqlite3

events = [
   'Западня',
   'Чертополох',
   #'Заговор',
   #'Долгожданная встреча'
]

async def transitionEvent(callback, chance):
   if random() <= chance:
      event = choice(events)
      if event == 'Западня':
         conn = sqlite3.connect('Base/data/transition_events.sql', check_same_thread=False)
         if conn.execute(f'SELECT Западня FROM transition_events WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 0:
            from apps.transition_events.events_content import event_1
            await event_1.start(callback)
         else:
            transitionEvent(callback, chance)
      elif event == 'Чертополох':
         conn = sqlite3.connect('Base/data/transition_events.sql', check_same_thread=False)
         if conn.execute(f'SELECT Чертополох FROM transition_events WHERE id_tg = {callback.message.chat.id}').fetchone()[0] == 0:
            from apps.transition_events.events_content import event_2
            await event_2.start(callback)
         else:
            transitionEvent(callback, chance)
      elif event == 'Заговор':
         pass
      elif event == 'Долгожданная встреча':
         pass
      else:
         pass