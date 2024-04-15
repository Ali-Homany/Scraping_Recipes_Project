import os
import time
import schedule
import threading
import telebot
from helper import MSGS, PATHS, get_ith_recipe_message


class ChefBot:
    def __init__(self):
        KEY = '7082579528:AAFtZCQeX-6x3x7N-0SnqPm_RDXD6XudKks'
        self.bot = telebot.TeleBot(KEY)

        @self.bot.message_handler(commands=['help', 'start'])
        def intro(message):
            chat_id = message.chat.id
            self.bot.send_message(chat_id=chat_id, text=MSGS.INTRO_MESSAGE)
        
        @self.bot.message_handler(commands=['subscribe'])
        def add_user(message):
            chat_id = message.chat.id
            try:
                subscribers = self.get_subscribers_ids()
                with open(PATHS.SUBSCRIBERS_FILE_PATH, 'a') as file:
                    if (str(chat_id) not in subscribers):
                        file.write(f'{chat_id}\n')
                        self.bot.send_message(chat_id=chat_id, text=MSGS.SUBSCRIBE_MESSAGE)
                    else:
                        self.bot.send_message(chat_id=chat_id, text=MSGS.ALREADY_SUBSCRIBED_MESSAGE)
            except Exception as e:
                print(e)
                self.bot.send_message(chat_id=chat_id, text=MSGS.ERROR_MESSAGE)
        
        @self.bot.message_handler(commands=['unsubscribe'])
        def remove_user(message):
            chat_id = message.chat.id
            try:
                subscribers = self.get_subscribers_ids()
                if (str(chat_id) not in subscribers):
                    self.bot.send_message(chat_id=chat_id, text=MSGS.NOT_SUBSCRIBED_MESSAGE)
                    return
                with open(PATHS.SUBSCRIBERS_FILE_PATH, 'w') as file:
                    subscribers.remove(str(chat_id))
                    file.writelines(subscribers)
                self.bot.send_message(chat_id=chat_id, text=MSGS.UNSUBSCRIBE_MESSAGE)
            except Exception as e:
                print(e)
                self.bot.send_message(chat_id=chat_id, text=MSGS.ERROR_MESSAGE)

    def get_subscribers_ids(self):
        with open(PATHS.SUBSCRIBERS_FILE_PATH, 'r') as file:
            subscribers = file.readlines()
        subscribers = [s.strip() for s in subscribers]
        return subscribers

    def send_todays_message(self):
        with open(PATHS.CURR_INDEX_FILE_PATH, 'r') as file:
            content = file.read()
            if content != '':
                index = int(content) + 1
            else:
                index = 0
        with open(PATHS.CURR_INDEX_FILE_PATH, 'w') as file:
            file.write(str(index))

        msg, photo_location = get_ith_recipe_message(index=index)
        subscribers = self.get_subscribers_ids()
        for subscriber_id in subscribers:
            if os.path.exists(photo_location):
                with open(photo_location, 'rb') as photo:
                    self.bot.send_photo(chat_id=subscriber_id, photo=photo)
            else:
                self.bot.send_message(chat_id=subscriber_id, text=photo_location)
            self.bot.send_message(chat_id=subscriber_id, text=msg)

    def schedule_daily_message(self):
        # schedule.every().day.at('15:00').do(self.send_todays_message)
        schedule.every(10).seconds.do(self.send_todays_message)
        while True:
            schedule.run_pending()
            time.sleep(10)

    def run(self):
        daily_recipe_thread = threading.Thread(target=self.schedule_daily_message)
        daily_recipe_thread.start()
        self.bot.polling()
