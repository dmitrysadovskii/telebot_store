# Компоненты для описания структуры таблиц
from sqlalchemy import Column, Integer, DateTime, ForeignKey
# Импортируем модули для связки таблиц
from sqlalchemy.orm import relationship, backref
# Импортируем модель Категории для связки моделей
from models.product import Products
from data_base.db_core import Base


class Orders(Base):
    """
    Класс-модель для описания таблицы "Заказы"
    основана на декларативном стиле SQLAlchemy
    """

    # Название таблицы
    __tablename__ = "orders"

    # Поля таблицы
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer)
    data = Column(DateTime)
    product_id = Column(Integer, ForeignKey('products.id'))
    user_id = Column(Integer)

    # Для каскадного удаления данных из таблицы
    category = relationship(
        Products,
        backref=backref('orders',
                        uselist=True,
                        cascade='delete, all')
    )

    def __str__(self):
        """
        Метод возвращает строковое представление объекта класса
        :return: str
        """
        return f"{self.quantity} {self.data}"
