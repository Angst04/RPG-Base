"""Этот код написан ChatGPT и требует проверки и доработки"""

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# States for the conversation
SELECT_OPPONENT, PLAYING = range(2)

# Dictionary to store user data and game state
user_data = {}

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher(bot)

# Command to start the game
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {"opponent": None, "score": 0}

    keyboard = InlineKeyboardMarkup().add(InlineKeyboardButton("Find Opponent", callback_data=str(SELECT_OPPONENT)))
    await message.reply("Welcome to the PvP game! Press 'Find Opponent' to start.", reply_markup=keyboard)

    return SELECT_OPPONENT

# Handler for selecting an opponent
@dp.callback_query_handler(lambda c: c.data == str(SELECT_OPPONENT))
async def select_opponent(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_data[user_id]["opponent"] = None

    await bot.edit_message_text("Searching for an opponent...", user_id, callback_query.message.message_id)

    # Basic matchmaking example: Find the first user also looking for an opponent
    for uid, data in user_data.items():
        if uid != user_id and data["opponent"] is None:
            # Opponent found!
            user_data[uid]["opponent"] = user_id
            user_data[user_id]["opponent"] = uid

            await bot.send_message(uid, f"Opponent found: {callback_query.from_user.username}. Game starting!")
            await bot.send_message(user_id, f"Opponent found: {data['opponent']}. Game starting!")

            # Display the initial score
            await display_score(uid, user_id)

            # Transition to the PLAYING state
            return

    # If no opponent is found, you may continue searching or handle it differently
    await bot.edit_message_text("No opponent found. Continue searching or try again later.", user_id,
                                callback_query.message.message_id)

# Handler for playing the game
@dp.message_handler(lambda message: message.text.lower() in ['increase', 'decrease'] and user_data.get(message.from_user.id))
async def play_game(message: types.Message):
    user_id = message.from_user.id
    opponent_id = user_data[user_id]["opponent"]

    # Example: Let's say the game involves increasing or decreasing the shared score
    user_input = message.text.lower()

    if user_input == 'increase':
        user_data[user_id]["score"] += 1
    elif user_input == 'decrease':
        user_data[user_id]["score"] -= 1

    # Display the updated score to both players
    await display_score(user_id, opponent_id)

async def display_score(player1_id, player2_id):
    score_player1 = user_data[player1_id]["score"]
    score_player2 = user_data[player2_id]["score"]

    await bot.send_message(player1_id, f"Your score: {score_player1}. Opponent's score: {score_player2}")
    await bot.send_message(player2_id, f"Your score: {score_player2}. Opponent's score: {score_player1}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
