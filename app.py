import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def bot_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<имя валюты><в какую валюту ' \
           'перевести><количество переводимой валюты>\nНапример:  евро рубль 1000\nУвидеть список всех доступных ' \
           'валют: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def converting(message: telebot.types.Message):
    try:
        values_carrency = message.text.split(' ')

        if len(values_carrency) > 3:
            raise ConvertionException('Слишком много параметров')
        if len(values_carrency) < 3:
            raise ConvertionException('Недостаточно параметров')

        base, quote, amount = values_carrency
        total_base = CurrencyConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Курс конвертации 1 {base} = {round(total_base, 5)} {quote}\n За {amount} {keys[base]} Вы получаете {round(total_base * float(amount), 2)} {keys[quote]} '
        bot.send_message(message.chat.id, text)


bot.polling()