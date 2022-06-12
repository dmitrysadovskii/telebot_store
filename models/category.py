# Компоненты для описания структуры таблиц
from sqlalchemy import Column, Integer, String, Boolean
from data_base.db_core import Base


class Category(Base):
    """
    Класс-модель для описания таблицы "Категория товаров"
    основана на декларативном стиле SQLAlchemy
    """

    # Название таблицы
    __tablename__ = "category"

    # Поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __str__(self):
        """
        Метод возвращает строковое представление объекта класса
        :return: str
        """
        return self.name
