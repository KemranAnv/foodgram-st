from django.core.management.base import BaseCommand
import csv
from core.models import Ingredient


class Command(BaseCommand):
    help = 'Загружает ингредиенты из CSV-файла'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Путь к CSV-файлу')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Ingredient.objects.get_or_create(
                        name=row[0],
                        measurement_unit=row[1]
                    )
                self.stdout.write(self.style.SUCCESS(
                    f'Ингредиенты успешно загружены из {csv_file_path}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(
                f'Файл {csv_file_path} не найден'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка: {str(e)}'))
