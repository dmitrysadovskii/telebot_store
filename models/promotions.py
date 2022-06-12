# Компоненты для описания структуры таблиц
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# Импортируем модули для связки таблиц
from sqlalchemy.orm import relationship, backref
# Класс-конструктор для работы с декларативным стилем работы с SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
# Импортируем модель Категории для связки моделей
from product import Products

# Инициализация декларативного стиля
Base = declarative_base()


class Promotions(Base):
    """
    Класс-модель для описания таблицы "Акции"
    основана на декларативном стиле SQLAlchemy
    """

    # Название таблицы
    __tablename__ = "promotions"

    # Поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    end_data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('product.id'))

    # Для каскадного удаления данных из таблицы
    category = relationship(
        Products,
        backref('promotions',
                uselist=True,
                cascade='delete, all')
    )

    def __str__(self):
        """
        Метод возвращает строковое представление объекта класса
        :return: str
        """
        return f"{self.quantity} {self.data}"
