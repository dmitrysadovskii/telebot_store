# импортируем базовый класс для наследования обработчика
import settings.message
from handlers.handler import Handler
# импортируем конфиги и настройки
from settings import config, utility
# импортируем сообщения для отображения в боте
from settings.message import MESSAGES


class HandlerAllText(Handler):
    """
    Класс обрабатывающий все сообщения от нажатия на кнопку
    """

    def __init__(self, bot):
        super(HandlerAllText, self).__init__(bot)
        self.order_number = 0

    def press_button_goods(self, message):
        """
        Обработка нажатия кнопки 'товары'
        :param message:
        :return:
        """
        self.bot.send_message(chat_id=message.chat.id, text='Каталог категории товаров',
                              parse_mode='HTML', reply_markup=self.keyboards.remove_menu())
        self.bot.send_message(chat_id=message.chat.id, text='Сделайте Свой выбор',
                              parse_mode='HTML', reply_markup=self.keyboards.category_menu())

    def press_button_info(self, message):
        """
        Обработка нажатия кнопки info
        :param message:
        :return:
        """
        self.bot.send_message(chat_id=message.chat.id, text=MESSAGES['trading_store'],
                              parse_mode='HTML', reply_markup=self.keyboards.info_menu())

    def press_button_back(self, message):
        """
        Обработка нажатия кнопку 'назад'
        :param message:
        :return:
        """
        self.bot.send_message(chat_id=message.chat.id, text='Вы вернулись назад',
                              parse_mode='HTML', reply_markup=self.keyboards.start_menu())

    def press_button_setting(self, message):
        """
        Обработка нажатия кнопку setting
        :param message:
        :return:
        """
        self.bot.send_message(chat_id=message.chat.id, text=MESSAGES['settings'],
                              parse_mode='HTML', reply_markup=self.keyboards.settings_menu())

    def press_button_product(self, message, product):
        """
        Обработка нажатия кнопку product
        :param message: object from message_handler
        :param product: product name
        :return:
        """
        self.bot.send_message(chat_id=message.chat.id, text=f'Категория {config.KEYBOARD[product]}',
                              reply_markup=self.keyboards.set_select_category(config.CATEGORY[product]))
        self.bot.send_message(chat_id=message.chat.id, text='Ok',
                              reply_markup=self.keyboards.category_menu())

    def press_button_order(self, message):
        """
        Обработка кнопки нажатия Заказы.
        Необходимо показать информацию о текущих заказах.
        :param message: object from message_handler
        :return:
        """
        # Создать переменную индекса номера заказа в бд
        self.order_number = 0
        # Взять все id заказов в виде списка
        order_id_list = self.DB.select_all_product_id_in_order()
        # Проверить, что корзина не пустая. Елси пустая, то вывести сообщение, что нет заказов в корзине
        if not order_id_list:
            self.bot.send_message(chat_id=message.chat.id, text=MESSAGES['no_orders'],
                                  parse_mode='HTML', reply_markup=self.keyboards.category_menu())
            return

        # По индексу взять необходимый для отображения id заказа из списка
        order_id = order_id_list[self.order_number]
        # Достать количество позиций товара в заказе
        quantity = self.DB.select_single_product_quantity_in_order(order_id)
        # Отправляем ответ пользователю
        self.send_message_order(order_id, quantity, message)

    def press_button_up(self, message):
        """
        Увеличить количество товаров на 1 единицу
        :param message: message of the current context user
        :return:
        """

        # Взять количество товаров в заказе по id
        product_ids = self.DB.select_all_product_id_in_order()
        product_id = product_ids[self.order_number]
        quantity_order = self.DB.select_single_product_quantity_in_order(product_id)
        # Взять количество товаров на складе по id
        quantity_product = self.DB.select_single_product_quantity(product_id)
        # Проверить, что количество товаров на складе больше 0
        if quantity_product > 0:
            quantity_product -= 1
            quantity_order += 1
        # Увеличить количество товара в заказе на 1
        update_field = "quantity"
        self.DB.update_product_value(product_id, update_field, quantity_product)
        # Уменьшить количество товара на складе на 1
        self.DB.update_order_value(product_id, update_field, quantity_order)
        self.send_message_order(product_id, quantity_order, message)

    def press_button_down(self, message):
        """
        Увеличить количество товаров на 1 единицу
        :param message: message of the current context user
        :return:
        """

        # Взять количество товаров в заказе по id
        product_ids = self.DB.select_all_product_id_in_order()
        product_id = product_ids[self.order_number]
        quantity_order = self.DB.select_single_product_quantity_in_order(product_id)
        # Взять количество товаров на складе по id
        quantity_product = self.DB.select_single_product_quantity(product_id)
        # Проверить, что количество товаров на складе больше 0
        if quantity_product > 0:
            quantity_product += 1
            quantity_order -= 1
        # Увеличить количество товара в заказе на 1
        update_field = "quantity"
        self.DB.update_product_value(product_id, update_field, quantity_product)
        # Уменьшить количество товара на складе на 1
        self.DB.update_order_value(product_id, update_field, quantity_order)
        self.send_message_order(product_id, quantity_order, message)

    def press_button_delete(self, message):
        """
        Удалить товар из заказа
        :param message:
        :return:
        """
        # Получить список всех id продуктов в заказе
        product_ids_in_order = self.DB.select_all_product_id_in_order()
        # Взять необходимый id по текущему ордеру
        if product_ids_in_order:
            product_id = product_ids_in_order[self.order_number]
            # Получить количество продуктов в заказе по id продукта
            quantity = self.DB.select_single_product_quantity_in_order(product_id)
            # Добавить количество продуктов в заказе на склад
            quantity_product = self.DB.select_single_product_quantity(product_id)
            quantity_product += quantity
            # Удалить количество продуктов в заказе с заказа
            self.DB.delete_order(product_id)
            product_quantity_field = 'quantity'
            self.DB.update_product_value(product_id, product_quantity_field, quantity_product)
            # Уменьшить счетчик заказов на 1
            self.order_number = self.order_number - 1 if self.order_number > 0 else 0

        # Выести предыдущий заказ, если есть
        product_ids_in_order = self.DB.select_all_product_id_in_order()
        print(f'product_ids_in_order: {product_ids_in_order}')
        if product_ids_in_order:
            product_id = product_ids_in_order[self.order_number]
            quantity_product = self.DB.select_single_product_quantity_in_order(product_id)
            self.send_message_order(product_id, quantity_product, message)
        # Выести сообщение о том что заказов нет, если нет :)
        else:
            print('NO PRODUCTS!')
            self.bot.send_message(chat_id=message.chat.id,
                                  text=MESSAGES['no_orders'],
                                  parse_mode='HTML',
                                  reply_markup=self.keyboards.category_menu())

    def press_button_next_order(self, message):
        """
        Показать следующий товар в заказе
        :param message:
        :return:
        """
        # Получить количество всех товаров в заказе
        amount_orders = self.DB.count_rows_orders()
        # Проверить, что текущий номер заказа не больше количества заказов и не равен последнему
        # Увеличить счетчик заказа, если не равен и не больше последнего
        if self.order_number < amount_orders - 1:
            self.order_number += 1
        # Вернуть сообщение о следующем заказе
        product_id = self.DB.select_all_product_id_in_order()[self.order_number]
        quantity_order = self.DB.select_single_product_quantity_in_order(product_id)
        self.send_message_order(product_id, quantity_order, message)

    def press_button_back_order(self, message):
        """
        Показать предыдущий товар в заказе
        :param message:
        :return:
        """
        if self.order_number > 0:
            self.order_number -= 1
        product_id = self.DB.select_all_product_id_in_order()[self.order_number]
        quantity_order = self.DB.select_single_product_quantity_in_order(product_id)
        self.send_message_order(product_id, quantity_order, message)

    def press_button_apply(self, message):
        # Получить количество каждого товара в заказе
        order_cost = utility.total_cost(self.DB)
        order_position_amount = self.DB.count_rows_orders()
        self.bot.send_message(chat_id=message.chat.id,
                              text=MESSAGES['apply'].format(order_cost,
                                                            order_position_amount),
                              parse_mode='HTML',
                              reply_markup=self.keyboards.category_menu())
        self.DB.delete_all_order()

    def send_message_order(self, product_id, quantity, message):
        """
        Вывести информацию об заказе
        :param product_id: product id which need to display from orders
        :param quantity: product quantity in orders
        :param message: message of the current context user
        :return:
        """
        # Вывести сообщение "Номер заказа order_number"
        self.bot.send_message(chat_id=message.chat.id, text=MESSAGES['order_number'].format(self.order_number + 1),
                              parse_mode='HTML')
        # Вывести инфу о заказе
        self.bot.send_message(chat_id=message.chat.id,
                              text=MESSAGES['order'].format(
                                  self.DB.select_single_product_name(product_id),
                                  self.DB.select_single_product_title(product_id),
                                  self.DB.select_single_product_price(product_id),
                                  quantity),
                              parse_mode='HTML', reply_markup=self.keyboards.order_menu(self.order_number, quantity))

    def handle(self):

        @self.bot.message_handler(func=lambda m: True)
        def handle(message):
            """
            Обработчик всех событий при нажатии на кнопку в боте
            :param message:
            :return:
            """
            "********** MENU **********"
            if message.text == config.KEYBOARD['CHOOSE_GOODS']:
                self.press_button_goods(message)

            if message.text == config.KEYBOARD['INFO']:
                self.press_button_info(message)

            if message.text == config.KEYBOARD['SETTINGS']:
                self.press_button_setting(message)

            if message.text == config.KEYBOARD['<<']:
                self.press_button_back(message)

            "********** SEMIPRODUCT, GROCERY, ICE_CREAM **********"
            if message.text == config.KEYBOARD['SEMIPRODUCT']:
                self.press_button_product(message, 'SEMIPRODUCT')

            if message.text == config.KEYBOARD['GROCERY']:
                self.press_button_product(message, 'GROCERY')

            if message.text == config.KEYBOARD['ICE_CREAM']:
                self.press_button_product(message, 'ICE_CREAM')

            if message.text == config.KEYBOARD['ORDER']:
                self.press_button_order(message)

            "********** MENU (ORDER) **********"
            if message.text == config.KEYBOARD['UP']:
                self.press_button_up(message)
            if message.text == config.KEYBOARD['DOWN']:
                self.press_button_down(message)
            if message.text == config.KEYBOARD['X']:
                self.press_button_delete(message)
            if message.text == config.KEYBOARD['NEXT_STEP']:
                self.press_button_next_order(message)
            if message.text == config.KEYBOARD['BACK_STEP']:
                self.press_button_back_order(message)
            if message.text == config.KEYBOARD['APPLY']:
                self.press_button_apply(message)
