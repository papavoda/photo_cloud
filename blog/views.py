from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.base import TemplateView
from .models import Category

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class CategoryListView(ListView):
    model = Category
    num_categories = Category.objects.count()
    template_name = 'blog/category_list.html'
    list_categories = Category.objects.all()
    queryset = Category.objects.all()
    context_object_name = 'my_category_list'

    def get_context_data(self, **kwargs):
        # В первую очередь получаем базовую реализацию контекста
        context = super(CategoryListView, self).get_context_data(**kwargs)
        # Добавляем новую переменную к контексту и инициализируем её некоторым значением
        context['num_cat'] = self.num_categories
        context['url'] = 'category/'
        return context
