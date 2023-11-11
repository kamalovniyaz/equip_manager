from django.core.paginator import Paginator
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from web.models import Equipment
from web.serializers import EquipmentSerializer


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
        Получение информации об оборудовании по ID.

        :param id: Id оборудования
        :return: Возвращает информацию об оборудовании в формате JSON.
        :raises: HTTP 404 - Если оборудование с указанным ID не найдено.
        """
        try:
            equipment_id = int(request.GET.get('id'))
            equipment = Equipment.objects.get(id=equipment_id)
            serializer = EquipmentSerializer(equipment)
            print(serializer.data)
            return Response(serializer.data)
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


class EquipmentListView(APIView):
    """
       Вывод пагинированного списка оборудования.
       Есть возможность поиска путем указания query параметров советующим ключам ответа

    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        search_param = request.GET.get('search', None)

        # Фильтрация объектов по параметру поиска, если он задан
        if search_param:
            equipments = Equipment.objects.filter(
                serial_number__icontains=search_param)
        else:
            equipments = Equipment.objects.all()

        paginator = Paginator(equipments, 10)  # показывать 10 строк на странице

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        total_items = paginator.count  # Общее количество элементов
        total_pages = paginator.num_pages  # Общее количество страниц
        serializer = EquipmentSerializer(page_obj, many=True)

        return JsonResponse(
            {
                "equipments": serializer.data,
                "totalItems": total_items,
                "totalPages": total_pages,
            }
        )
