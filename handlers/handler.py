from abc import ABCMeta, abstractmethod
# импортируем класс разметки в телеграмм боте
from markup.markup import Markup
# импортируем класс-менеджер для работы с библиотекой
from data_base.dbalchemy import ManagerDB


# metaclass необходим что бы переопределить инициализация унаследованных классов
class Handler(metaclass=ABCMeta):
    """
    Базовый класс от которого наследуются все обработчики
    """
    def __init__(self, bot):
        # получаем объект бота
        self.bot = bot
        # инициализируем разметку кнопок
        self.keyboards = Markup()
        # инициализируем менеджер для работы с db
        self.DB = ManagerDB()

    @abstractmethod
    def handle(self):
        """
        Метод опрабоки событий.
        :return:
        """
        pass