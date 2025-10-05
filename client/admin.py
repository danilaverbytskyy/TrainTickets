from django.contrib import admin
from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    # Поля, отображаемые в списке объектов
    list_display = [
        'full_name',
        'birth_date',
        'passport',
        'phone',
        'user',
        'created_at'
    ]

    # Поля для поиска
    search_fields = [
        'first_name',
        'last_name',
        'patronymic',
        'passport',
        'phone'
    ]

    # Фильтры в правой части экрана
    list_filter = [
        'birth_date',
        'created_at'
    ]

    # Поля, которые можно редактировать прямо из списка
    list_editable = [
        'phone'
    ]

    # Поля в форме создания/редактирования, сгруппированные по смыслу
    fieldsets = [
        ('Основная информация', {
            'fields': (
                ('first_name', 'last_name', 'patronymic'),
                'birth_date',
                'user'
            )
        }),
        ('Контакты и документы', {
            'fields': (
                'phone',
                'passport',
            )
        }),
        ('Служебная информация', {
            'fields': (
                'created_at',
                'updated_at',
            ),
            'classes': ('collapse',)  # Свернутый блок
        })
    ]

    # Автоматическое заполнение slug (если бы было такое поле)
    # prepopulated_fields = {"slug": ("first_name", "last_name")}

    # Только для чтения в форме редактирования
    readonly_fields = [
        'created_at',
        'updated_at'
    ]

    def full_name(self, obj):
        """Возвращает полное имя клиента."""
        components = [obj.last_name, obj.first_name, obj.patronymic]
        return ' '.join(filter(None, components)).strip()

    full_name.short_description = 'Полное имя'
