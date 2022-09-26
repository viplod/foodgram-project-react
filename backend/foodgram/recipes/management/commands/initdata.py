import csv
import os.path

from django.core.management.base import BaseCommand, CommandError

from foodgram.settings import STATICFILES_DIRS
from recipes.models import Ingredient


def get_model_csv_filename():
    csv_file = 'ingredients.csv'
    file_path = f'{STATICFILES_DIRS[0]}data/{csv_file}'
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
                print(name, measurement_unit)
                try:
                    Ingredient.objects.update_or_create(
                        name=name,
                        measurement_unit=measurement_unit,
                    )
                except Exception:
                    raise CommandError('Can`t create model "%s"' % name)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully load model `{name}`, '
                    f'create {count + 1} row in database.')
            )
