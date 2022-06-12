def convert(list_with_tuples):
    """
    convert [(1,),(2,)] -> (1,2)
    :return: (int)
    """
    return [item[0] for item in list_with_tuples]


def total_cost(DB):
    """
    Вернуть финальную цену для заказа
    :param quantities:
    :param prices:
    :return:
    """
    product_ids_order = DB.select_all_product_id_in_order()
    all_prices = [DB.select_single_product_price(product_id)
                  for product_id in product_ids_order]
    all_quantities_order = [DB.select_single_product_quantity_in_order(product_id)
                            for product_id in product_ids_order]
    quantities_prices = zip(all_quantities_order, all_prices)
    final_cost = map(lambda quantity_price: quantity_price[0] * quantity_price[1],
                     quantities_prices)
    return sum(final_cost)
