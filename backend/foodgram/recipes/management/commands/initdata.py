import csv
import os.path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from recipes.models import Ingredient


def get_model_csv_filename():
    csv_file = 'ingredients.csv'
    data_dir = os.path.join(settings.BASE_DIR, 'data')
    file_path = f'{data_dir}/{csv_file}'
    return file_path if os.path.isfile(file_path) else None


class Command(BaseCommand):
    """Класс для работы с кастомными менеджмент командами"""
    help = 'Loads initial data for models'

    def handle(self, *args, **options):
        file = get_model_csv_filename()
        if not file:
            self.stdout.write(
                self.style.ERROR(
                    f'Error loads model: Ingredient from file: {file}'
                )
            )

        with open(file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for count, row in enumerate(reader):
                name, measurement_unit = row
                try:
                    Ingredient.objects.update_or_create(
                        name=name,
                        measurement_unit=measurement_unit,
                    )
                except Exception:
                    raise CommandError(f'Can`t create model {name}')

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully load model `{name}`, '
                    f'create {count + 1} row in database.')
            )
