from datetime import datetime
from os import path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# импортируем класс отвечающий за перенос моделей на структуру базы данных
from .db_core import Base
from models.product import Products
from models.order import Orders

from settings import utility
from settings.config import DATABASE


class Singleton(type):
    """
    Класс синголтон предоставляет механизм создания одного
    и только одного объекта класса, предоставляя к нему
    глобальную точку доступа
    """

    # При инициализации класса синголтон будет вызван init и переопределен type.
    # Объект type отвечает за создание объектов.
    def __init__(cls, name, bases, *args):
        super(Singleton, cls).__init__(name, bases, *args)
        cls.__instance = None

    # При инициализации будет вызван метод call, который создаст экземпляр вызываемого класса
    # или вернет уже созданный класс
    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.__instance


class ManagerDB(metaclass=Singleton):
    """
    Класс менеджер для работы с db
    """

    def __init__(self):
        # создаем движок дб
        self.engine = create_engine(DATABASE)
        # создаем объект сессии
        session = sessionmaker(bind=self.engine)
        self._session = session()
        if not path.isfile(DATABASE):
            # metadata содержит объекты всех унаследованных моделей от Base
            Base.metadata.create_all(self.engine)

    def select_all_product_category(self, category):
        """
        Вернуть все товары по категории
        :param category: category id
        :return:
        """
        result = self._session.query(Products).filter_by(
            category_id=category).all()
        self.close()
        return result

    def add_order(self, quantity, product_id, user_id):
        """
        Метод добавления заказа в дб
        :param quantity:
        :param product_id:
        :param user_id:
        :return:
        """
        # получить все product_id в бд заказов, так как продукт мог бы заказан ранее
        # мы хотим не создавать новую запись, а увеличить количество продукта
        all_product_id = self.select_all_product_id_in_order(user_id)
        # проверяем если ли текущий продукт в уже заказанных
        if product_id in all_product_id:
            # добавляем к текущему заказу продукта количество заказанного продекта
            quantity_product_in_order = self.select_single_product_quantity_in_order(product_id)
            quantity_product_in_order += quantity
            self.update_order_value(product_id, 'quantity', quantity_product_in_order)
            # удаляем количетсво заказанного продукта со склада
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= quantity
            self.update_product_value(product_id, 'quantity', quantity_product)
            return
        else:
            # создаем новыую запись в заказе
            order = Orders(quantity=quantity, product_id=product_id,
                           user_id=user_id, data=datetime.now())
            quantity_product = self.select_single_product_quantity(product_id)
            quantity_product -= quantity
            self.update_product_value(product_id, 'quantity', quantity_product)

        # добавить объект заказа в сессия
        self._session.add(order)
        self._session.commit()
        self.close()

    def select_all_product_id_in_order(self, user_id=1):
        """
        Вернуть все id продуктов в заказе
        :user_id: User ID who added to order
        :return: list[int]
        """
        all_product_id_in_orders = self._session.query(Orders.product_id).filter_by(user_id=user_id).all()
        return utility.convert(all_product_id_in_orders)

    def select_single_product_quantity(self, product_id):
        """
        Вернуть количество продукта на складе
        :param product_id:
        :return:
        """
        result = self._session.query(Products.quantity).filter_by(id=product_id).one()
        self.close()
        return result.quantity

    def update_product_value(self, product_id, field_name, value):
        """
        Обновляет количество товара на складе
        в соответствии с номером товара - product_id
        :param product_id:
        :param field_name:
        :param value:
        :return:
        """
        self._session.query(Products).filter_by(id=product_id).update({field_name: value})
        self._session.commit()
        self.close()

    def select_single_product_quantity_in_order(self, product_id):
        """
        Возвращает количества продукта в заказе
        :param product_id:
        :return:
        """
        result = self._session.query(Orders.quantity).filter_by(product_id=product_id).one()
        self.close()
        return result.quantity

    def update_order_value(self, product_id, field_name, quantity_product_in_order):
        """
        Обновляем количества товара в заказе
        :param product_id:
        :param field_name:
        :param quantity_product_in_order:
        :return:
        """
        self._session.query(Orders).filter_by(product_id=product_id).update(
            {field_name: quantity_product_in_order})
        self._session.commit()
        self.close()

    def select_single_product_name(self, product_id):
        """
        Вернуть имя продукта
        :param product_id:
        :return:
        """
        result = self._session.query(Products.name).filter_by(id=product_id).one()
        self.close()
        return result.name

    def select_single_product_title(self, product_id):
        """
        Вернуть заголовок продукта
        :param product_id:
        :return:
        """
        result = self._session.query(Products.title).filter_by(id=product_id).one()
        self.close()
        return result.title

    def select_single_product_price(self, product_id):
        """
        Вернуть заголовок продукта
        :param product_id:
        :return:
        """
        result = self._session.query(Products.price).filter_by(id=product_id).one()
        self.close()
        return result.price

    def count_rows_orders(self):
        """
        Вернуть количество записей в заказе
        :return:
        """
        orders_amount = self._session.query(Orders).count()
        self.close()
        return orders_amount

    def delete_order(self, product_id):
        """
        Удалить продукт в заказе по id продукта
        :param product_id: id продукта
        :return:
        """
        self._session.query(Orders).filter_by(product_id=product_id).delete()
        self._session.commit()
        self.close()

    def delete_all_order(self):
        """
        Удалить все заказы в корзине
        :return:
        """
        product_ids = self.select_all_product_id_in_order()
        for product_id in product_ids:
            self.delete_order(product_id)
        # map(self.delete_order, product_ids)

    def close(self):
        self._session.close()
