import telebot
from telebot import types
import logging
from data.buttons import MainMenu
from data.config import *

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(TOKEN)

def check_auth(message):
    """Проверка авторизации"""
    if message.from_user.id != USER_ID:
        bot.reply_to(message, "Извините, этот бот приватный.")
        return False
    return True

def main_menu():
    """Создание главного меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(*MainMenu.ALL)
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    """Обработчик команды /start"""
    if not check_auth(message):
        return

    logger.info(f"Пользователь {message.from_user.id} запустил бота")

    bot.send_message(message.chat.id,
                     "Привет! Я бот для отслеживания тренировок и питания.\nВыбери действие в меню:",
                     reply_markup=main_menu()
                     )
@bot.message_handler(func=lambda message: message.text == MainMenu.WORKOUT)
def workout(message):
    """Временный обработчик тренировок"""
    if not check_auth(message):
        return

    logger.info("Переход в раздел тренировок")
    bot.send_message(message.chat.id,
                     "Раздел тренировок в разработке. Скоро здесь можно будет записывать подходы!"
                     )
@bot.message_handler(func=lambda message: True)
def echo(message):
    """Временный обработчик всего остального"""
    if not check_auth(message):
        return

    logger.info(f"Получено сообщение: {message.text}")
    bot.send_message(message.chat.id,
                     f"Ты написал: {message.text}\n\nИспользуй кнопки меню для навигации."
                     )

if __name__ == '__main__':
    logger.info("Бот запускается...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Ошибка: {e}")