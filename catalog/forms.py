from django import forms

from .models import Product

# Константа с запрещёнными словами
FORBIDDEN_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "description", "image", "category", "purchase_price", "is_published"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            else:
                field.widget.attrs["class"] = "form-control"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        self._check_forbidden_words(name, "название")
        return name

    def clean_description(self):
        description = self.cleaned_data.get("description", "")
        self._check_forbidden_words(description, "описание")
        return description

    def clean_purchase_price(self):
        price = self.cleaned_data.get("purchase_price")
        if price is not None and price < 0:
            raise forms.ValidationError("Цена не может быть отрицательной.")
        return price

    def _check_forbidden_words(self, text, field_verbose):
        """Проверяет, что в тексте нет запрещённых слов (без учёта регистра)."""
        if text:
            lower_text = text.lower()
            for word in FORBIDDEN_WORDS:
                if word in lower_text:
                    raise forms.ValidationError(f'Слово "{word}" запрещено в {field_verbose}.')
