import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
bot = telebot.TeleBot('7866999033:AAHIDFptopNsvFBc00DXKvM7dPc0Q_gkL0Y')


# Команда /start
@bot.message_handler(commands=['start'])
def start_command(message):
    # Создаем клавиатуру с кнопкой "Отправить номер телефона"
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    phone_button = KeyboardButton("Отправить номер телефона", request_contact=True)
    markup.add(phone_button)

    bot.send_message(message.chat.id, "Привет! Нажмите на кнопку ниже, чтобы отправить номер телефона.",
                     reply_markup=markup)


# Обработчик получения контакта
@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None:
        # Получаем номер телефона из сообщения
        phone_number = message.contact.phone_number
        bot.send_message(message.chat.id, f"Спасибо! Ваш номер телефона: {phone_number}")
    else:
        bot.send_message(message.chat.id, "Не удалось получить номер телефона. Попробуйте еще раз.")


# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
