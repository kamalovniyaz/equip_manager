from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models import Equipment
from web.serializers import EquipmentSerializer
from web.services.get_equip_type_with_pagination import get_equipment_types
from web.services.get_equip_with_pagination import get_equipments


# Create your views here.


class EquipmentManagement(APIView):
    """
    Обработчик для CRUD операций с оборудованием.

    Attributes:
        id (int): Идентификатор оборудования.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Получение информации об оборудовании. Если в get параметре есть Id, то выполняем получение одного элемента.
        Если нет, то возвращаем пагинированный список.

        :param id: Id оборудования
        :return: Возвращает информацию об оборудовании в формате JSON.
        :raises: HTTP 404 - Если оборудование с указанным ID не найдено.
        """
        try:
            equipment_id = request.GET.get('id', None)
            if equipment_id:
                queryset = Equipment.objects.get(id=int(equipment_id))
                serializer_class = EquipmentSerializer(queryset)

                return Response({"equipment": serializer_class.data})
            else:
                search_param = request.GET.get('search', None)
                page_number = request.GET.get("page")

                # Получение данных через пагинацию и с фильтрацией по параметру
                equipments, total_items, total_pages = get_equipments(page_number, search_param)

                return JsonResponse(
                    {
                        "equipments": equipments,
                        "total_items": total_items,
                        "total_pages": total_pages,
                    }
                )
        except Equipment.DoesNotExist:
            return Response("Equipment not found", status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Создание новой записи об оборудовании

        :return: Возвращает информацию об оборудовании в формате JSON.
        :raises: HTTP 400 - Если отправленные данные не валидны.
        """
        serializer = EquipmentSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid() and serializer.validate_serial_numbers():
            serializer.create(request.data)
            return Response("The equipment has been successfully created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Обновление информации об оборудовании

        :param id: Id оборудования
        :return: Возвращает информацию об оборудовании в формате JSON.
        :raises:
            HTTP 404 - Если оборудование с указанным ID не найдено.
            HTTP 400 - Если данные не прошли валидацию.

        """
        try:
            equipment_id = int(request.GET.get('id'))
            equipment = Equipment.objects.get(id=equipment_id)
            serializer = EquipmentSerializer(equipment, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Equipment.DoesNotExist:
            return Response("Equipment not found", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        """
        "Мягкое" удаление оборудования

        :param id: Id оборудования
        :return: Возвращает код успешного выполнения операции.
        :raises:
            HTTP 404 - Если оборудование с указанным ID не найдено.
            HTTP 400 - Если данные не прошли валидацию.

        """
        try:
            equipment_id = int(request.GET.get('id'))
            equipment = Equipment.objects.get(id=equipment_id)
            equipment.is_active = False
            equipment.save()
            return Response("Equipment deleted", status=status.HTTP_204_NO_CONTENT)
        except Equipment.DoesNotExist:
            return Response("Equipment not found", status=status.HTTP_404_NOT_FOUND)


class EquipmentTypesListView(APIView):
    """
       Вывод пагинированного списка оборудования.
       Есть возможность поиска путем указания query параметров советующим ключам ответа

    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_param = request.GET.get('search', None)
        page_number = request.GET.get("page")

        # Получение данных через пагинацию и с фильтрацией по параметру
        equipment_types, total_items, total_pages = get_equipment_types(page_number, search_param)

        return JsonResponse(
            {
                "equipment_types": equipment_types,
                "total_items": total_items,
                "total_pages": total_pages,
            }
        )
