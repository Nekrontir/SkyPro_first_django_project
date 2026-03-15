from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Product, Category


class Command(BaseCommand):
    help = 'Удаляет все продукты и категории, затем загружает тестовые данные из фикстур'

    def handle(self, *args, **options):

        self.stdout.write("Удаляем существующие данные...")
        Product.objects.all().delete()
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Продукты и категории удалены."))


        self.stdout.write("Загружаем фикстуры...")
        try:
            call_command('loaddata', 'category.json')
            call_command('loaddata', 'product.json')
            self.stdout.write(self.style.SUCCESS("Фикстуры успешно загружены."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при загрузке фикстур: {e}"))

        self.stdout.write(self.style.SUCCESS("Команда выполнена успешно!"))