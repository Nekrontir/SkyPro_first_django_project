from django.core.cache import cache
from catalog.models import Product

def get_products_by_category(category_id):
    """
    Возвращает список (list) опубликованных продуктов категории.
    Использует низкоуровневое кеширование с ключом 'category_{id}'.
    """
    cache_key = f"category_{category_id}"
    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.filter(
                category_id=category_id,
                is_published=True
            ).select_related('category')
        )
        cache.set(cache_key, products, timeout=600)

    return products