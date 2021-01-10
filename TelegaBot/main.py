import telebot
from extension import API,ApiExeptions
from config import keys,TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start','help'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, список возможностей: \n "
                                      "/values - доступные валюты \n"
                                      "формат запроса : <ИМЯ ВАЛЮТЫ ЦЕНУ КОТОРОЙ ХОТИТЕ УЗНАТЬ>\n"
                                      "<ИМЯ ВАЛЮТЫ В КАКОЙ ИНТЕРЕСУЕТ ЦЕНА ПЕРВОЙ>\n"
                                      "<КОЛИЧЕСТВО ПЕРВОЙ ВАЛЮТЫ>\n"
                                      "ПРИМЕР: доллар рубль 10 <-вернет цену 10 долларов в рублях ")

@bot.message_handler(commands=['values'])
def values(message :telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text,key,))
    bot.reply_to(message,text)
@bot.message_handler(content_types=['text', ])
def convert(message:telebot.types.Message):
    try:
        values = message.text.split(' ')
        quote, base, amount = values
        if len(values) != 3:
            raise ApiExeptions('Слишком много параметров')
        total_base = API.get_price(quote,base, amount)
    except ApiExeptions as e:
        bot.reply_to(message,f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base}-{total_base}'
        bot.send_message(message.chat.id,text)
bot.polling()