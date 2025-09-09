import telebot
import random
import requests

import DATA_Center
import shop

from telebot import types

bot_token_api = "8305303302:AAGtXs6IFJFd_JuZRDDLmaehpiDbzhu6kxc"

bot = telebot.TeleBot(bot_token_api)

dm = DATA_Center.Data_Manager()
DATA_Status = dm.Load() # True or False

random_messages = ["Привет, я бот-помощник!", "42 брат.", "Ряльна", "Homosapianssapians"]

clicks = {}

sticker_ids = [
    "CAACAgIAAxkBAAESHXRovv9wyYOht8narIrkhywNbcTghAACe00AAh_-QUlWY0PosQKs_TYE",
    "CAACAgIAAxkBAAESHW5ovv8fC7uFkmx5c4BN7BdUeGy5zQACTzkAAulVBRgDRCJieYcAAfU2BA",
    "CAACAgIAAxkBAAERo4xoqd4fdqj78cvpj4db50ugFbJsYAACFQADwDZPE81WpjthnmTnNgQ",
    "CAACAgIAAxkBAAESHXJovv8w_gTxHIxtYL1wrBE_1oIHAQAConwAAjILuEld-RVZsJopazYE",
    "CAACAgIAAxkBAAESJTdowDGVN6CazKNQ3I1zg6ALULwj2AACdHYAAjDw2Uh_GaQxFNs4EzYE",
    "CAACAgIAAxkBAAESJThowDGVkyv4oT3GPmS-KbJnE2a-XwACzkgAAgEw2UmLv5YL5kQf3zYE",
    "CAACAgIAAxkBAAESJTlowDGVt81P_mbaJjC3V5ALxq_S6wACXRQAArbxeUuKkJI_Pig01zYE",
    "CAACAgIAAxkBAAESJTpowDGVDMHb8fyF4p-3XE65MUjIswACS04AArKJAUttFn4BTCRPeTYE",
    "CAACAgIAAxkBAAESJTtowDGVXbctnsHt91fdZM540hCBwwACMVsAAp2hCUoIEdoftTljlDYE",
    "CAACAgIAAxkBAAESJUNowDIWYu3tHZOkKKL8xp2YWVpXrwACMCcAAmo2sEou3TNaP0m_MzYE",
    "CAACAgIAAxkBAAESJURowDIW4r41AAE41t2pqTZDkFEpU7gAAvkRAAJrY6FI7CS9-1CuIOM2BA",
    "CAACAgIAAxkBAAESJUVowDIWwAcZVHs80jxD7dqu9qoe4gACRwEAAntOKhAtvk07cY4gsDYE",
    "CAACAgIAAxkBAAESJUZowDIWLg9DLJDoab89rJca_W20sQAC4SQAArwW8El9ug4AAUNDCYc2BA",
    "CAACAgIAAxkBAAESJUdowDIWbHN0d0PIiqh80feOvKNK-AACEEcAAoQ_cEuS4B9v_JycOjYE",
]
helpmsg = """
[__________Help___________]
/help - Помощь по командам
/credits - Кредиты
/shop - Магазин
/me - Профиль
/click - Кликнуть (+1 клик)
r_msg - Случайное сообщение
r_stick - Случайный стикер
r_num (1-100) - Случайное число
getText [url] - получает текст из сслыки на файл
[_________________________]
                     """

def get_bot_info():
    url = f"https://api.telegram.org/bot{bot_token_api}/getMe"
    response = requests.get(url)
    data = response.json()
    if data.get('ok'):
        return data['result']['first_name'], data['result']['username']
    else:
        raise Exception(f"Ошибка: {data.get('description')}")

@bot.message_handler(commands= ['help', 'hlp', 'помощь'])
def help_cmd(message):
    bot.send_message(message.from_user.id, helpmsg)
@bot.message_handler(func=lambda message: message.text.lower() == 'помощь')
def help_cmd(message):
    bot.send_message(message.from_user.id, helpmsg)

@bot.message_handler(commands = ['start'])
def start_cmd(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/help")
    markup.add(btn1)
    dm.SetData(message.from_user.id)
    bot.send_message(message.from_user.id, "Привет. Я бот помощник, учусь выполнять вские разные функции. Если интересно, жми на кнопку снизу.", reply_markup=markup)

@bot.message_handler(commands = ['credits'])
def credits_cmd(message):
    bot.send_message(message.from_user.id, """
[_________Информация об авторе_________]
@Jere2009 - Основатель
@Vldmrlksv - Тестер
[_________________________]
                     """)

@bot.message_handler(func=lambda message: message.text.lower() == 'r_msg')
def rmsg_cmd(message):
    selected_msg = random.choice(random_messages)
    bot.reply_to(message, selected_msg)
 
@bot.message_handler(func=lambda message: message.text.lower() == 'r_num')
def rnum_cmd(message):
    selected_msg = str(random.randint(1,100))
    bot.reply_to(message, selected_msg)

@bot.message_handler(func=lambda message: message.text.lower() == 'r_stick')
def rstick_cmd(message):
    if sticker_ids:  # Проверяем, есть ли стикеры в списке
        selected_sticker = random.choice(sticker_ids)
        bot.send_sticker(message.chat.id, selected_sticker)
    else:
        bot.reply_to(message, "Стикеры не настроены. Добавьте ID стикеров в код.")
@bot.message_handler(commands=['user', 'profile', 'me'])
def profile_cmd(message):
    user = message.from_user
    bot.reply_to(message, f"""
[---------Profile---------]
User: {user.first_name} {user.last_name}
Clicks: {dm.GetData(user.id, "clicks")}
Stars: {dm.GetData(user.id, "stars")}
[_________________________]
                     """)
@bot.message_handler(commands=['click', 'clck'])
def click_cmd(message):
    user = message.from_user
    clicks = dm.GetData(user.id, "clicks")
    clicks += 1
    dm.SetData(user.id, "clicks", clicks)
    bot.reply_to(message,"Click +1")
items = shop.GetShop()
@bot.message_handler(commands=['admin209', 'ad09'])
def admin_cmd(message):
    user = message.from_user
    s = dm.GetData(user.id, "stars")
    s += 4000
    dm.SetData(user.id, "stars", s)
    bot.reply_to(message,"⭐ +4000")
items = shop.GetShop()
@bot.callback_query_handler(func=lambda call: call.data.startswith('buy_'))
def handle_buy_callback(call):
    item_id = call.data.replace('buy_', '')
    status_buy = shop.BuyItem(item_id, dm.GetData(call.from_user.id, "stars"))
    if status_buy == True:
        g = dm.GetData(call.from_user.id, "stars")
        g -= int(items[item_id]["price"])
        dm.SetData(call.from_user.id, "stars", g)
        bot.send_message(call.from_user.id, f"Успешно куплен. {item_id}")
    elif status_buy == False:
        bot.send_message(call.from_user.id, f"Невозможно купить {item_id}.\nНедостаточно средств.")
    return
@bot.message_handler(commands=['shop', 'store', 'shp'])
def shop_cmd(message):
    user = message.from_user
    bot.send_message(message.from_user.id, "[-----Магазин-----]")
    for i in items:
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(f"Купить {items[i]["price"]} {items[i]["currency"]}", callback_data=f"buy_{i}")
        markup.add(btn1)
        bot.send_message(message.from_user.id, items[i]["msg"], reply_markup=markup)
botname, botusername = get_bot_info()
print("Current bot is:")
print(botname)
print("@" + botusername)
print(f"Data load status: {DATA_Status}")
bot.polling(none_stop=True, interval=0) # DONT DELETE THIS