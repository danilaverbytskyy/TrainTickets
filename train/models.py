from django.db import models


class Train(models.Model):
    title = models.CharField(max_length=100, blank=False, unique=True)
    capacity = models.PositiveIntegerField(default=0, null=False)
    city_from = models.CharField()
    city_to = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "Поезд"
        verbose_name_plural = 'Поезды'

    def __str__(self):
        return self.title
