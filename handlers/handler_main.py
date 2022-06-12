# импортируем класс обработчика команд
from handlers.handler_commands import HandlerCommands
from handlers.handler_all_text import HandlerAllText
from handlers.handler_inline_query import HandlerInlineQuery


class HandlerMain:
    """
    Класс компоновщик
    """

    def __init__(self, bot):
        # получаеам бота
        self.bot = bot
        # инициализируем создание обработчика команд
        self.handler_commands = HandlerCommands(self.bot)
        # инициализируем обработчик всех команд от кнопок
        self.handler_all_text = HandlerAllText(self.bot)
        # инициализируем обработчик всех команд от инлайн кнопок
        self.handler_inline_query = HandlerInlineQuery(self.bot)

    def handle(self):
        self.handler_commands.handle()
        self.handler_all_text.handle()
        self.handler_inline_query.handle()
