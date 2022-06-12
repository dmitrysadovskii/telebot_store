# импортируем базовый класс для наследования обработчика
from handlers.handler import Handler


class HandlerCommands(Handler):
    """
    Класс обрабатывает входящие команды /start, /stop и др
    """

    def __init__(self, bot):
        # переопределяем бота для обработчика команд
        super(HandlerCommands, self).__init__(bot)

    def press_button_start(self, message):
        """
        Обрабатывает входящие /start комманды
        :return:
        """
        self.bot.send_message(chat_id=message.chat.id,
                              text=f"{message.from_user.first_name}, Здарова! Что прикажете делать?",
                              reply_markup=self.keyboards.start_menu())

    def handle(self):
        """
        Обработчик сообщений (декорабор),
        который обрабатывает start комманды
        :return:
        """
        @self.bot.message_handler(commands=["start"])
        def handle(message):
            if message.text == "/start":
                self.press_button_start(message)
