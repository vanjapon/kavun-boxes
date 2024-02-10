import telebot
from telebot import types
import json
import random
import time

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=80)

def keep_alive():
    t = Thread(target=run)
    t.start()

last_request_time = {}
user_info = {}

def update_loot():
    return {
        'loot1': random.randint(1, 3),
        'loot2': random.randint(3, 5),
        'loot3': random.randint(5, 10),
        'loot4': random.randint(10, 15),
        'loot5': random.randint(15, 25),
        'loot6': random.randint(25, 40),
        'loot7': random.randint(40, 70),
        'loot8': random.randint(150, 300),
        'loot9': random.randint(700, 1500)
    }

video_messages_commonbox = {
    'Видео 1 обычный бокс': {'сообщение': 'дододо\nобычный\n+{loot1} арбузов🍉', 'arbuzy_key': 'loot1'},
    'Видео 2 обычный бокс': {'сообщение': 'скромный манке\nобычный\n+{loot2} арбузов🍉', 'arbuzy_key': 'loot2'},
    'Видео 3 обычный бокс': {'сообщение': 'джентельмен манке\nнеобычный\n+{loot3} арбузов🍉', 'arbuzy_key': 'loot3'},
    'Видео 4 обычный бокс': {'сообщение': 'манке на велике\nнеобычный\n+{loot4} арбузов🍉', 'arbuzy_key': 'loot4'},
    'Видео 5 обычный бокс': {'сообщение': 'ммм молочко\nредкий\n+{loot5} арбузов🍉', 'arbuzy_key': 'loot5'},
    'Видео 6 обычный бокс': {'сообщение': 'аааа рапек\nредкий\n+{loot6} арбузов🍉', 'arbuzy_key': 'loot6'},
    'Видео 7 обычный бокс': {'сообщение': 'новогодний пон\nэпический\n+{loot7} арбузов🍉', 'arbuzy_key': 'loot7'},
    'Видео 8 обычный бокс': {'сообщение': 'модный манке\nлегендарный\n+{loot8} арбузов🍉', 'arbuzy_key': 'loot8'},
    'Видео 9 обычный бокс': {'сообщение': 'рыбак манке\nпасхалочка\n+{loot9} арбузов🍉', 'arbuzy_key': 'loot9'}
}

video_chances_commonbox = {
    'Видео 1 обычный бокс': 0.75,
    'Видео 2 обычный бокс': 0.6,
    'Видео 3 обычный бокс': 0.53,
    'Видео 4 обычный бокс': 0.4,
    'Видео 5 обычный бокс': 0.33,
    'Видео 6 обычный бокс': 0.26,
    'Видео 7 обычный бокс': 0.12,
    'Видео 8 обычный бокс': 0.03,
    'Видео 9 обычный бокс': 0.001
}

video_paths_commonbox = {
    'Видео 1 обычный бокс': 'дододо.MP4',
    'Видео 2 обычный бокс': 'скромни манке.MP4',
    'Видео 3 обычный бокс': 'джентельмен манке.MP4',
    'Видео 4 обычный бокс': 'манке на велике.MP4',
    'Видео 5 обычный бокс': 'ммм малачко.MP4',
    'Видео 6 обычный бокс': 'аааа рапек.mp4',
    'Видео 7 обычный бокс': 'навагодни пон.mp4',
    'Видео 8 обычный бокс': 'модни манке.mp4',
    'Видео 9 обычный бокс': 'рыбак манке.mp4'
}

def load_user_info():
    try:
        with open('user_info.json', 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("Файл user_info не найден или ошибка декодирования JSON. Возвращается пустой словарь.")
        return {}
    except Exception as e:
        print(f"Ошибка при загрузке user_info: {e}")
        return {}

def save_user_info():
        try:
            with open('user_info.json', 'w') as file:
                json.dump(user_info, file)
        except Exception as e:
            print(f"Ошибка при сохранении user_info: {e}")

open('user_info.json', 'a').close()
user_info = load_user_info()

def change_user_info(user_id, username=None, watermelons=0, redeemed_promo_reliz=None):
    global user_info

    try:
        with open('user_info.json', 'r') as file:
            user_info = json.load(file)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        print("User_info file not found or JSON decode error. Continuing with the existing data.")

    user_data = user_info.setdefault(user_id, {'username': None, 'watermelons': 0, 'redeemed_promo_reliz': 0})

    print(f"Before update - user_data: {user_data}")

    if username is not None:
        user_data['username'] = username

    user_data['watermelons'] += watermelons

    if redeemed_promo_reliz is not None:
        user_data['redeemed_promo_reliz'] = redeemed_promo_reliz

    print(f"After update - user_data: {user_data}")

    try:
        with open('user_info.json', 'w') as file:
            json.dump(user_info, file)
    except Exception as e:
        print(f"Error saving user_info: {e}")

bot = telebot.TeleBot('6700775574:AAE8TFF8yCYHpHkDN59rZuCbubibBHPCBDE')

@bot.message_handler(commands=['start'])
def start_handler(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('📦Открыть обычный Бокс')
    button2 = types.KeyboardButton('🍌Наш чатик')
    button3 = types.KeyboardButton('🍉Баланс арбузов')
    button4 = types.KeyboardButton('❓Редкости')
    markup.add(button1, button2)
    markup.add(button3, button4)
    bot.send_message(message.chat.id, f'Добро пожаловать в арбузные боксы, {message.from_user.first_name}!\nИспользуй промокод /reliz в честь релиза бота!', reply_markup=markup)

@bot.message_handler(commands=['reliz'])
def reliz_promo(message):
    global user_info
    user_id = str(message.from_user.id)
    user_data = user_info.get(user_id, {})
    promo_redeemed = user_data.get('redeemed_promo_reliz', 0)
    if promo_redeemed == 1:
        bot.send_message(message.chat.id, 'Ты уже вводил промо!')
    else:
        change_user_info(user_id, username=message.from_user.username, watermelons=100, redeemed_promo_reliz=1)
        bot.send_message(message.chat.id, 'Вы ввели промо и получили 100 арбузов!')

@bot.message_handler(content_types=['text'])
def cmds(message):
    print(f"Получено сообщение: {message.text}")
    if message.text == '🍌Наш чатик':
        bot.send_message(message.chat.id, 'https://t.me/arbuzerichat')
    elif message.text == '📦Открыть обычный Бокс':
        last_request = last_request_time.get(message.chat.id, 0)
        current_time = time.time()
        time_remaining = max(0, 5 - (current_time - last_request))
        if time_remaining > 0:
            bot.send_message(message.chat.id, f'Подождите ещё {time_remaining:.1f} секунд перед следующим кликом!')
            return

        print("Открывается обычный бокс...")
        last_request_time[message.chat.id] = current_time
        user_id = str(message.from_user.id)
        video_to_send = random.choices(list(video_chances_commonbox.keys()), weights=list(video_chances_commonbox.values()))[0]

        if video_to_send in video_messages_commonbox:
            loot = update_loot()
            change_user_info(user_id, username=message.from_user.username, watermelons=loot[video_messages_commonbox[video_to_send]['arbuzy_key']])

            current_message = video_messages_commonbox[video_to_send]['сообщение'].format(**loot)
            markup = types.ReplyKeyboardRemove()

            markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton('📦Открыть обычный Бокс')
            button2 = types.KeyboardButton('🍌Наш чатик')
            button3 = types.KeyboardButton('🍉Баланс арбузов')
            button4 = types.KeyboardButton('❓Редкости')
            markup2.add(button1, button2)
            markup2.add(button3, button4)

            bot.send_message(message.chat.id, 'Видео отправляется...\nЕсли сразу не отправилось, то подождите 5-10 сек.', reply_markup=markup)
            bot.send_video(message.chat.id, open(video_paths_commonbox[video_to_send], 'rb'), caption=current_message, reply_markup=markup2)
            print(f"Отправлено видео: {video_to_send}")
        else:
            bot.send_message(message.chat.id, 'Неизвестное видео!')
            print(f"Неизвестное видео: {video_to_send}")

    elif message.text == '🍉Баланс арбузов':
        global user_info
        user_id = str(message.from_user.id)
        user_data = user_info.get(user_id, {})
        watermelon_balance = user_data.get('watermelons', 0)
        bot.send_message(message.chat.id, f'У тебя {watermelon_balance} арбузов')
    elif message.text == '❓Редкости':
        bot.send_message(message.chat.id, 'Обычный: 75-60%\nНеобычный: 53-40%\nРедкий: 33-26%\nЭпический: 12%\nЛегендарный: 3%\nТакже можно найти секретного монке о котором тут не говорится')

keep_alive()
bot.polling()