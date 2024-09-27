import telebot
from decimal import *
from telebot import types
from config import TOKEN, keys
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    chao = (f'Привет <b>{message.from_user.first_name}</b>\nдля начала работы воспользуйтесь кнопками:\n'
            f'<b>Помощь</b> и'
            f'<b> Список валют</b>\n * если на экране не видно кнопок - закройте клавиатуру.')
# Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton('Помощь')
    button2 = types.KeyboardButton('Список валют')
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id, chao, parse_mode='html', reply_markup=markup)


#Получение сообщений от пользователя
@bot.message_handler(content_types=['text'])
def handle_text(message):
    # Если пользователь нажал Помощь
    if message.text.strip() == 'Помощь':
        answer = (f'Введите в одну строчку через пробел следующие данные:\n<i>1. название конвертируемой валюты</i> \
             <i>2. название валюты в которую конвертировать</i>\n<i>3. количество валюты для конвертации</i>\n * '
                  f'название валюты возьмите из <b>Списка валют</b>')
        # Отсылаем пользователю сообщение в его чат
        bot.send_message(message.chat.id, answer, parse_mode='html')
    # Если пользователь нажал Список валют
    elif message.text.strip() == 'Список валют':
        answer = ''
        for key in keys.keys():
            answer = '\n'.join(keys)
        # Отсылаем пользователю сообщение в его чат
        bot.send_message(message.chat.id, answer)
    #Обрабатываем запрос на конвертацию
    else:
        try:
            elements = message.text.split(' ')
            if len(elements) != 3:
                raise APIException('Количество введенных параметров не равно 3')
            quote, base, amount = elements
            quote, base = quote.lower(), base.lower()
            conv_num = CurrencyConverter.get_price(quote, base.lower(), amount)
        except APIException as e:
            bot.reply_to(message, f'Ошибка пользователя\n{e}')
        except Exception as e:
            bot.reply_to(message,f'Не удалось обработать команду\n{e}')
        else:
            number = float(conv_num) * float(amount)
            if number > 0.004:
                total = Decimal(number)
                total = total.quantize(Decimal("1.00"))
            else:
                total = number
            text = f'Стоимость покупки <U>{amount} {base}</U> составит <U>{total} {quote}</U>'
            bot.send_message(message.chat.id, text, parse_mode='html')


bot.polling(non_stop=True)