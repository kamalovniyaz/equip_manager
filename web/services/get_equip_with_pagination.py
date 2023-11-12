from django.core.paginator import Paginator

from web.models import Equipment
from web.serializers import EquipmentSerializer


def get_equipments(page_number, search_param):
    """
    Метод для получения данных с пагинацией.

    :param search_param: Параметр по которому осуществляется поиск
    :return: equipments_data, total_items, total_pages
    """
    # Фильтрация объектов по параметру поиска, если он задан
    if search_param:
        equipments = Equipment.objects.filter(
            serial_number__contains=search_param)
    else:
        equipments = Equipment.objects.all()

    paginator = Paginator(equipments, 10)  # показывать 10 строк на странице

    page_obj = paginator.get_page(page_number)

    total_items = paginator.count  # Общее количество элементов
    total_pages = paginator.num_pages  # Общее количество страниц
    serializer = EquipmentSerializer(page_obj, many=True)
    equipments_data = serializer.data

    return equipments_data, total_items, total_pages