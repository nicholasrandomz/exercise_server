import asyncio
import time
import datetime

from telethon import TelegramClient, events
from telethon import utils

import exercise
import quote
import logging

# =========== Telethon SETUP
api_id = 3847570
api_hash = 'df01d430acacb3b89085c58827f7f67a'
bot_token = '1806488135:AAEDFm7VmhCMxNXBnfqk-f7b4F85tQ1-BsI'
bot = TelegramClient('bot', api_id, api_hash)
bot.start(bot_token=bot_token)
# Bot PM user_id = 1806488135 PeerUser
# TAF Club PM chat_id = 487366831 PeerChat
# =========== LOGGING SETUP
file = str(datetime.datetime.now().date()) + ".log"
logging.basicConfig(filename=file, filemode='a', format='%(message)s', level=logging.INFO)
logging.info("ONLY INFO LEVEL")
# =========== EXERCISE DATABASE SETUP
ExerciseDatabase = exercise.ExerciseDatabase('exercise.json')
WeeklyChallenge = exercise.Challenge()
# =========== QUOTE DATABASE SETUP
QuoteGenerator = quote.QuoteDatabase('quote.json')
past_day = datetime.date.today()
logging.info("Starting Day - " + str(past_day))
DailyQuoteSent = False
# =========== TIME SETUP
while True:
    current_time = datetime.datetime.now()
    if current_time.second == 0:
        break

    time.sleep(1)

help_text = "Hello! Simply put, every week a new challenge is set for everyone in the group to complete. " \
            "Help contribute in exercising! No 'good or bad', 'strong or weak', just your best to be a better you!" \
            "\n\n" \
            "This is entirely honor-based, and the only reward is a community and stronger you"

@bot.on(events.NewMessage(chats="TAF Club"))
# returns message type
async def my_event_handler(event):
    # print(event.from_id)
    chat_entity = await bot.get_entity(event.peer_id)
    sent_entity = await bot.get_entity(event.from_id)
    logging.info("USER - " + utils.get_display_name(sent_entity) + " - " + event.text)

    if "/help" in event.text:
        await bot.send_message(chat_entity, help_text)
        logging.info("BOT - UserHelp - " + str(help_text))
    elif "/challenge" in event.text:
        await bot.send_message(chat_entity, WeeklyChallenge.challenge_text())
        logging.info("BOT - UserChallenge - " + str(WeeklyChallenge.challenge_text()))
    elif "/status" in event.text:
        await bot.send_message(chat_entity, WeeklyChallenge.status_text())
        logging.info("BOT - UserStatus - " + str(WeeklyChallenge.status_text()))
    elif "/add" in event.text:
        if not WeeklyChallenge.isCompleted:
            text = str(event.text).split(' ')
            try:
                WeeklyChallenge.AddAmount(utils.get_display_name(sent_entity), float(text[1]))
            except ValueError as V:
                text = "@" + utils.get_display_name(sent_entity) + " Invalid Amount"
                await bot.send_message(chat_entity, text)
                logging.info("BOT - UserAdd - " + str(text))
        await bot.send_message(chat_entity, WeeklyChallenge.status_text())
        logging.info("BOT - UserAdd - " + str(WeeklyChallenge.status_text()))
    elif "/leaderboard" in event.text:
        await bot.send_message(chat_entity, WeeklyChallenge.leaderboard_text())
        logging.info("BOT - UserLeaderboard - " + str(WeeklyChallenge.leaderboard_text()))
    elif "/update" in event.text:
        text = str(event.text).split(' ')
        WeeklyChallenge.UpdateAmount(text[1], int(text[2]))
        await bot.send_message(chat_entity, WeeklyChallenge.status_text())
        logging.info("BOT - AdminUpdate - " + str(WeeklyChallenge.status_text()))

async def clock():
    global past_day, DailyQuoteSent
    while True:
        today = datetime.date.today()
        if today != past_day:
            DailyQuoteSent = False
            past_day = today
        if not DailyQuoteSent:
            current_time = datetime.datetime.now()

            if current_time.hour == 12 and current_time.minute == 2:  # Send at 12.02AM
                chat_entity = await bot.get_entity(1806488135)  # TAF Club chat_id
                await bot.send_message(chat_entity, QuoteGenerator.GetQOTD())
                logging.info("BOT - QOTD - " + str(QuoteGenerator.GetQOTD()) + " at " + str(today))
                DailyQuoteSent = True
        await asyncio.sleep(60)

print("Bot Started")
asyncio.get_event_loop().create_task(clock())
bot.run_until_disconnected()
