from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .forms import ProductForm
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")
