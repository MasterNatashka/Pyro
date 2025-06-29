from django.db import models


class Location(models.Model):
    name = models.CharField("Название", max_length=30)
    def __str__(self):
        return self.name
    class Meta():
        verbose_name = "Участок"
        verbose_name_plural = "Участки"

class Camera(models.Model):
    name = models.CharField("Название", max_length=40)
    address = models.CharField("Адрес", max_length=40)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, verbose_name="Участок")
    def __str__(self):
        return f"{self.name} - {self.address}"
    class Meta():
        verbose_name = "Видеокамера"
        verbose_name_plural = "Видеокамеры"
