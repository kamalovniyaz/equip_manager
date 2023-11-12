from django.db import models


class EquipmentType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(verbose_name='Наименование типа', max_length=100)
    serial_number_mask = models.CharField(verbose_name='Маска серийного номера', max_length=50)

    def __str__(self):
        return self.name


class Equipment(models.Model):
    id = models.AutoField(primary_key=True)
    equipment_type = models.CharField(verbose_name='Тип оборудования', max_length=50)
    serial_number = models.CharField(verbose_name='Серийный номер', max_length=50, unique=True)
    is_active = models.BooleanField(verbose_name='Активно', default=True)
    note = models.TextField(verbose_name='Примечание', null=True)

    class Meta:
        unique_together = ('equipment_type', 'serial_number') # Связка уникальных полей

    def __str__(self):
        return self.serial_number

