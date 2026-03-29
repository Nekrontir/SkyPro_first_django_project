from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import BlogPostForm
from .models import BlogPost


class BlogListView(ListView):
    """Список статей – только опубликованные"""

    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "blog_posts"

    def get_queryset(self):
        """Фильтруем по признаку публикации"""
        return BlogPost.objects.filter(is_published=True)


class BlogDetailView(DetailView):
    """Детальный просмотр статьи – увеличиваем счётчик просмотров"""

    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "blog_post"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save(update_fields=["views_count"])
        return obj


class BlogCreateView(CreateView):
    """Создание статьи"""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:blog_list")


class BlogUpdateView(UpdateView):
    """Редактирование статьи"""

    model = BlogPost
    form_class = BlogPostForm
    template_name = "blog/blog_form.html"

    def get_success_url(self):
        """После успешного редактирования – на страницу статьи"""
        return reverse_lazy("blog:blog_detail", kwargs={"pk": self.object.pk})


class BlogDeleteView(DeleteView):
    """Удаление статьи"""

    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:blog_list")
