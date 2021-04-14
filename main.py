import telebot

from tele_bot.weather import get_current_weather, get_daily_forecast
from config import TOKEN


bot = telebot.TeleBot(TOKEN)

hideBoard = telebot.types.ReplyKeyboardRemove()  # if sent as reply_markup, will hide the keyboard
# Bot handler section

@bot.message_handler(commands=['start'])
def command_start(message):
    # Somehow to check for running commands?
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    start_markup.row('/start', '/help', '/hide')
    start_markup.row('/myid', '/weather')
    bot.send_message(message.chat.id, "🤖 The bot has started!\n⚙ Enter /help to see bot's function's")
    bot.send_message(message.from_user.id, "⌨️ The Keyboard is added!\n⌨️ /hide To remove kb ", reply_markup=start_markup)


@bot.message_handler(commands=['hide'])
def hide_keyboard(message):
    bot.send_message(message.chat.id, "Keyboard is no more!", reply_markup=hideBoard)


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id,'Only /weather , /myid commands available right now')


@bot.message_handler(commands=['myid'])
def test_command(message):
    usr_id = message.chat.username
    bot.send_message(message.chat.id, f'Your username is @{usr_id}')


@bot.message_handler(commands=['weather'])
def weather_command(message):
    city_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    city_markup.row('Moscow', 'Saint-Petersburg')
    city_markup.row('Yalta', 'Istanbul')

    msg = bot.send_message(message.chat.id,
                           'Please choose city',
                           reply_markup=city_markup)
    bot.register_next_step_handler(msg, process_weather_step1)


def process_weather_step1(message):
    city = message.text
    forecast_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    forecast_markup.row('Current', 'Daily')
    msg = bot.send_message(message.chat.id,
                           f'Showing weather in {city}. \nDo you '
                           f'want current weather or daily forecast?', reply_markup=forecast_markup)
    bot.register_next_step_handler(msg, process_weather_step2, city)


def process_weather_step2(message, city):
    try:
        if message.text.lower() == 'current':
            forecast = get_current_weather(city)
            bot.reply_to(message, forecast)
        elif message.text.lower() == 'daily':
            forecast = get_daily_forecast(city)
            bot.reply_to(message, forecast)
        elif message.text.lower() == 'stop':
            bot.send_message(message.chat.id, "Choose another command")
        else:
            msg = bot.send_message(message.chat.id, 'Please type "current" or "daily"!')
            bot.register_next_step_handler(msg, process_weather_step1)
    except Exception as e:
        bot.reply_to(message, 'oops')


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling(none_stop=True)




