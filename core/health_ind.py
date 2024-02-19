async def health_ind(amount, builder):
   tens_count = amount // 10
   amount %= 10
   fives_count = amount // 5
   amount %= 5
   
   builder.button(text='HP:', callback_data='info_hp')

   for _ in range(tens_count):
      builder.button(text='❤️×10', callback_data='info_hp')
      
   for _ in range(fives_count):
      builder.button(text='❤️×5', callback_data='info_hp')

   for _ in range(amount):
      builder.button(text='❤️', callback_data='info_hp')
      
   return builder