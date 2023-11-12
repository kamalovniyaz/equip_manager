from django.core.paginator import Paginator

from web.models import Equipment, EquipmentType
from web.serializers import EquipmentSerializer, EquipmentTypeSerializer


def get_equipment_types(page_number, search_param):
    """
    Метод для получения данных о типе оборудования с пагинацией.

    :param search_param: Параметр по которому осуществляется поиск
    :return: equipments_type_data, total_items, total_pages
    """
    # Фильтрация объектов по параметру поиска, если он задан
    if search_param:
        equipments = EquipmentType.objects.filter(
            name__icontains=search_param)
    else:
        equipments = EquipmentType.objects.all()

    paginator = Paginator(equipments, 10)  # показывать 10 строк на странице

    page_obj = paginator.get_page(page_number)

    total_items = paginator.count  # Общее количество элементов
    total_pages = paginator.num_pages  # Общее количество страниц
    serializer = EquipmentTypeSerializer(page_obj, many=True)
    equipments_types_data = serializer.data

    return equipments_types_data, total_items, total_pages