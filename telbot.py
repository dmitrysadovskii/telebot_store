# импортируем функцию создания телеграм бота
from telebot import TeleBot
# импортируем основные настройки и конфиги
from settings import config
# импортируем главный класс-обработчик бота
from handlers.handler_main import HandlerMain


class TelBot:
    """
    Основной класс телеграмм бота (сервер), в основе которого
    служит библиотека pyTelegramBotAPI
    """

    __version__ = config.VERSION
    __author__ = config.AUTHOR

    def __init__(self):
        # берем токен из конфига
        self.token = config.TOKEN
        # инициализируем бота на основе токена
        self.bot = TeleBot(self.token)
        # инициализируем обработчик событий для данного бота
        self.handler = HandlerMain(self.bot)

    def start(self):
        """
        Метод для запуска обработчиков событий для бота
        :return:
        """
        self.handler.handle()

    def run_bot(self):
        # запускаем обработчики событий для бота
        self.start()
        # служит для запуска бота в режиме нон-стоп
        self.bot.polling(none_stop=True)


if __name__ == "__main__":
    bot = TelBot()
    bot.run_bot()
