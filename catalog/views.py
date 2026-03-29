from django.shortcuts import render
from django.views.generic import DetailView, ListView, TemplateView

from .models import Product


class ProductListView(ListView):
    """Контроллер для отображения списка продуктов"""

    model = Product
    template_name = "home.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    """Контроллер для отображения одного продукта"""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ContactsView(TemplateView):
    """Контроллер для страницы контактов"""

    template_name = "contacts.html"
