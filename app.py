import telebot
from config import keys, list_of_currencies, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'Start', 'help', 'Help'])
def bot_help(message: telebot.types.Message):
    text = f'Привет, {message.chat.username}! Чтобы начать работу введите команду боту одной строкой в следующем ' \
           f'формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nНапример: евро рубль ' \
           f'1000\nУвидеть список всех доступных валют: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values', 'Values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in list_of_currencies.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converting(message: telebot.types.Message):
    try:
        values_carrency = message.text.split(' ')

        if len(values_carrency) > 3:
            raise ConvertionException('Слишком много параметров\n/help')
        if len(values_carrency) < 3:
            raise ConvertionException('Недостаточно параметров\n/help')

        base, quote, amount = values_carrency
        total_base = round(CurrencyConverter.get_price(base, quote, amount), 5)
        total_quote = round(total_base * float(amount), 2)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Курс конвертации 1 {base} = {total_base} {quote}\n За {amount} {keys[base]} Вы получаете {total_quote} {keys[quote]} '
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
