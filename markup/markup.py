# импортируем специальные типы телеграм телеграмм бота для создания элементов интерфейса
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
# импортируем настройки и конфиги
from settings import config
# импортируем класс-менеджер для работы с db
from data_base.dbalchemy import ManagerDB


class Markup:
    """
    Класс отвечает за разметку и созданию объектов на странице
    """

    # Инициализация разметки
    def __init__(self):
        self.markup = None
        # Создаем экземпляр класса-менеджера db
        self.DB = ManagerDB()

    def set_button(self, name, order_number=0, quantity=0):
        """
        Создает и возвращает кнопку на странице по имени
        :param name: имя кнопки в конфиге
        :param order_number: номер заказа в корзине
        :param quantity: количество товара в заказе
        :return:
        """

        if name == 'AMOUNT_PRODUCT':
            config.KEYBOARD[name] = f'{quantity}'

        if name == 'AMOUNT_ORDERS':
            orders_amount = self.DB.count_rows_orders()
            config.KEYBOARD[name] = f'{order_number + 1} из {orders_amount}'

        return KeyboardButton(config.KEYBOARD[name])

    def start_menu(self):
        """
        Метод для создания меню при вводе команды start в боте
        :return: ReplyKeyboardMarkup
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_button_1 = self.set_button('CHOOSE_GOODS')
        item_button_2 = self.set_button('INFO')
        item_button_3 = self.set_button('SETTINGS')
        self.markup.row(item_button_1)
        self.markup.row(item_button_2, item_button_3)
        return self.markup

    def info_menu(self):
        """
        Меню отображения при нажатии на кнопку инфо
        :return: ReplyKeyboardMarkup
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_button_1 = self.set_button('<<')
        self.markup.row(item_button_1)
        return self.markup

    def settings_menu(self):
        """
        Меню отображения при нажатии на кнопку настройки
        :return: ReplyKeyboardMarkup
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_button_1 = self.set_button('<<')
        self.markup.row(item_button_1)
        return self.markup

    def remove_menu(self):
        """
        Удаляет данные кнопки и возвращает ее
        :return: ReplyKeyboardRemove
        """
        return ReplyKeyboardRemove()

    def category_menu(self):
        """
        Показывает меню категории товаров
        :return:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_button_1 = self.set_button('SEMIPRODUCT')
        item_button_2 = self.set_button('GROCERY')
        item_button_3 = self.set_button('ICE_CREAM')
        item_button_4 = self.set_button('<<')
        item_button_5 = self.set_button('ORDER')
        self.markup.add(item_button_1)
        self.markup.add(item_button_2)
        self.markup.add(item_button_3)
        self.markup.row(item_button_4, item_button_5)
        return self.markup

    @staticmethod
    def set_inline_button(name):
        """
        Создает и возвращает кнопку по входным параметрам
        :return:
        """
        return InlineKeyboardButton(str(name),
                                    callback_data=str(name.id))

    def set_select_category(self, category):
        """
        Создать инлайн разметку выбранной категории товара и вернуть разметку
        :param category:
        :return:
        """
        self.markup = InlineKeyboardMarkup(row_width=1)
        # Перебираем элементы модели полученные из базы данных по продукту
        for item in self.DB.select_all_product_category(category):
            self.markup.add(self.set_inline_button(item))
        return self.markup

    def order_menu(self, order_number, product_quantity):
        """
        Создает и возвращает меню упраления заказами
        :return:
        """
        self.markup = ReplyKeyboardMarkup(True, True)
        item_button_1 = self.set_button('X', order_number, product_quantity)
        item_button_2 = self.set_button('DOWN', order_number, product_quantity)
        item_button_3 = self.set_button('AMOUNT_PRODUCT', order_number, product_quantity)
        item_button_4 = self.set_button('UP', order_number, product_quantity)

        item_button_5 = self.set_button('BACK_STEP', order_number, product_quantity)
        item_button_6 = self.set_button('AMOUNT_ORDERS', order_number, product_quantity)
        item_button_7 = self.set_button('NEXT_STEP', order_number, product_quantity)

        item_button_8 = self.set_button('<<', order_number, product_quantity)
        item_button_9 = self.set_button('APPLY', order_number, product_quantity)

        self.markup.row(item_button_1, item_button_2, item_button_3, item_button_4)
        self.markup.row(item_button_5, item_button_6, item_button_7)
        self.markup.row(item_button_8, item_button_9)

        return self.markup
