from handlers.handler import Handler
from settings.message import MESSAGES


class HandlerInlineQuery(Handler):
    """
    Класс обработчик инлайн полей
    """

    def __init__(self, bot):
        super(HandlerInlineQuery, self).__init__(bot)

    def press_button_product(self, call, code):
        self.DB.add_order(1, code, 1)
        # модальное окно показывающие после выбора инлайн товара
        self.bot.answer_callback_query(call .id,
                                       MESSAGES['product_order'].format(
                                           self.DB.select_single_product_name(code),
                                           self.DB.select_single_product_title(code),
                                           self.DB.select_single_product_price(code),
                                           self.DB.select_single_product_quantity(code)),
                                       show_alert=True
                                       )

    def handle(self):
        """
        Метод обработчик нажатия инлайн полей
        :return:
        """

        @self.bot.callback_query_handler(func=lambda m: True)
        def handle(call):
            code = call.data
            if code.isdigit():
                code = int(code)
                self.press_button_product(call, code)
