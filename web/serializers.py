import re

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from web.models import Equipment, EquipmentType


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Переопределенный метод для проверки пользователя и выдачи ему JWT токена
    """

    username_field = "email"

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs[self.username_field],
            "password": attrs["password"],
        }
        try:
            from django.contrib.auth.models import User
            user = User.objects.get(email=credentials["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User with given email and password does not exists"
            )

        if not user.check_password(credentials["password"]):
            raise serializers.ValidationError("Invalid password")
        data = {}
        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class EquipmentTypeSerializer(serializers.ModelSerializer):
    """
    Сериализация типов оборудования
    """

    class Meta:
        model = EquipmentType
        fields = "__all__"


class EquipmentSerializer(serializers.ModelSerializer):
    """
    Сериализация модели оборудования
    """

    class Meta:
        model = Equipment
        fields = "__all__"

    def create(self, validated_data):
        Equipment.objects.create(equipment_type=validated_data.get('equipment_type'),
                                 serial_number=validated_data.get('serial_number'))
        return True

    def validate_serial_numbers(self):
        """
        Метод для проверки валидности маски оборудования.
        :return: True or ValidationError
        """
        # Получаем данные оборудования из входных данных
        equipment_type = self.initial_data.get('equipment_type')
        serial_number = self.initial_data.get('serial_number')

        # Получаем валидную маску для этого типа оборудования
        try:
            equip_type = EquipmentType.objects.get(name=equipment_type)
        except EquipmentType.DoesNotExist:
            raise serializers.ValidationError("Неподдерживаемый тип оборудования")

        # Создание регулярного выражения для каждой позиции в маске
        regex_patterns = {
            'N': r'\d',  # Цифра от 0 до 9
            'A': r'[A-Z]',  # Прописная буква латинского алфавита
            'a': r'[a-z]',  # Строчная буква латинского алфавита
            'X': r'[A-Z\d]',  # Прописная буква латинского алфавита или цифра от 0 до 9
            'Z': r'[-_@]'  # Символ из списка: "-", "_", "@"
        }

        # Проверка серийного номера с помощью соответствующей маски
        if re.match('^' + ''.join([regex_patterns.get(char, '.') for char in equip_type.serial_number_mask]) + '$',
                    serial_number):
            return True
        else:
            raise serializers.ValidationError(f"Серийный номер {serial_number} не соответствует маске")
