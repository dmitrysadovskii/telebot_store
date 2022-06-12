import os
# импортируем модуль emoji для отображения эмоджи
from emoji import emojize

# Токен выданный при регистрации
TOKEN = '5371412300:AAHonsGR0uU61QSLxI4bJGu4_yvgas-eo-s'
# Название БД
NAME_DB = 'products.db'
# Версия приложения
VERSION = '0.0.1'
# Автор приложения
AUTHOR = 'User'

# Родительская директория
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Путь до базы данных
DATABASE = os.path.join(f'sqlite:///{BASE_DIR}', NAME_DB)

COUNT = 0

# Кнопки управления
KEYBOARD = {
    'CHOOSE_GOODS': emojize(':open_file_folder: Выбрать товар'),
    'INFO': emojize(':speech_balloon: О магазине'),
    'SETTINGS': emojize('⚙️ Настройки'),
    'SEMIPRODUCT': emojize(':pizza: Полуфабрикаты'),
    'GROCERY': emojize(':bread: Бакалея'),
    'ICE_CREAM': emojize(':shaved_ice: Мороженое'),
    '<<': emojize('⏪'),
    '>>': emojize('⏩'),
    'BACK_STEP': emojize('◀️'),
    'NEXT_STEP': emojize('▶️'),
    'ORDER': emojize('✅ ЗАКАЗ'),
    'X': emojize('❌'),
    'DOWN': emojize('🔽'),
    'AMOUNT_PRODUCT': COUNT,
    'AMOUNT_ORDERS': COUNT,
    'UP': emojize('🔼'),
    'APPLY': '✅ Оформить заказ',
    'COPY': '©️'
}

# ID категории продукта
CATEGORY = {
    'SEMIPRODUCT': 1,
    'GROCERY': 2,
    'ICE_CREAM': 3
}

# Название команд
COMMANDS = {
    'START': 'start',
    'HELP': 'help'
}