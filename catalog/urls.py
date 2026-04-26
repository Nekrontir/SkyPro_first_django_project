from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import (ContactsView, ProductCreateView, ProductDeleteView, ProductDetailView, ProductListView,
                           ProductUpdateView,unpublish_product)

from django.views.decorators.cache import cache_page

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="home"),
    path("contacts/", ContactsView.as_view(), name="contacts"),
    path("product/<int:pk>/",cache_page(60 * 15)(ProductDetailView.as_view()), name="product_detail"),
    path("product/create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update/", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    path('product/<int:pk>/unpublish/', unpublish_product, name='product_unpublish'),
]
