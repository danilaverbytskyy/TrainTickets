from django.core.management.base import BaseCommand
from client.models import Client
from faker import Faker
import random
from datetime import datetime


class Command(BaseCommand):
    help = 'Создает 500 тестовых клиентов с пустыми пользователями'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=500,
            help='Количество клиентов для создания',
        )

    def handle(self, *args, **options):
        count = options['count']
        fake = Faker('ru_RU')

        # Список для более реалистичных телефонных кодов операторов
        phone_codes = ['901', '902', '903', '904', '905', '906', '915', '916', '917', '919',
                       '920', '921', '922', '923', '924', '925', '926', '927', '928', '929',
                       '930', '931', '932', '933', '934', '936', '937', '938', '939', '950',
                       '951', '952', '953', '954', '955', '956', '958', '960', '961', '962',
                       '963', '964', '965', '966', '967', '968', '969', '970', '971', '980',
                       '981', '982', '983', '984', '985', '986', '987', '988', '989']

        clients_created = 0

        for i in range(count):
            try:
                # Генерируем данные клиента
                gender = random.choice(['male', 'female'])
                if gender == 'male':
                    first_name = fake.first_name_male()
                    last_name = fake.last_name_male()
                    patronymic = fake.middle_name_male()
                else:
                    first_name = fake.first_name_female()
                    last_name = fake.last_name_female()
                    patronymic = fake.middle_name_female()

                # Генерируем номер телефона
                phone_code = random.choice(phone_codes)
                phone_number = fake.random_number(digits=7, fix_len=True)
                phone = f"+7{phone_code}{phone_number}"

                # Создаем клиента с явно указанным user=None
                client = Client(
                    first_name=first_name,
                    last_name=last_name,
                    patronymic=patronymic,
                    user=None,  # Все клиенты без пользователя
                    birth_date=fake.date_of_birth(minimum_age=18, maximum_age=80),
                    passport=f'{fake.random_number(digits=4)} {fake.random_number(digits=6)}',
                    phone=phone
                )
                client.save()
                clients_created += 1

                # Выводим прогресс каждые 50 записей
                if clients_created % 50 == 0:
                    self.stdout.write(
                        self.style.SUCCESS(f'Создано {clients_created} клиентов...')
                    )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка при создании клиента {i}: {e}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {clients_created} клиентов с пустыми пользователями')
        )
