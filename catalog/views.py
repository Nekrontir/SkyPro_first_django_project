from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import ProductForm
from .models import Product, Category
from .services import get_products_by_category


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


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return obj.owner == user or user.groups.filter(name='Модератор продуктов').exists()

@permission_required('catalog.can_unpublish_product', raise_exception=True)
def unpublish_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_published = False
    product.save()
    return redirect('catalog:product_detail', pk=pk)


class CategoryProductListView(ListView):
    """Список продуктов конкретной категории."""
    template_name = "category_products.html"
    context_object_name = "products"

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        # Сохраняем категорию, чтобы использовать в контексте
        self.category = get_object_or_404(Category, pk=category_id)
        return get_products_by_category(category_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        return context