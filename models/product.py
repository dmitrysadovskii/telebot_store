# Компоненты для описания структуры таблиц
from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
# Импортируем модули для связки таблиц
from sqlalchemy.orm import relationship, backref
# Импортируем модель Категории для связки моделей
from .category import Category
from data_base.db_core import Base


class Products(Base):
    """
    Класс-модель для описания таблицы "Товар"
    основана на декларативном стиле SQLAlchemy
    """

    # Название таблицы
    __tablename__ = "products"

    # Поля таблицы
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    title = Column(String)
    price = Column(Float)
    quantity = Column(Integer)
    is_active = Column(Boolean)
    category_id = Column(Integer, ForeignKey('category.id'))

    # Для каскадного удаления данных из таблицы
    category = relationship(
        Category,
        backref=backref('products',
                        uselist=True,
                        cascade='delete,all')
    )

    def __str__(self):
        """
        Метод возвращает строковое представление объекта класса
        :return: str
        """
        return f"{self.name} {self.title} {self.price}"
