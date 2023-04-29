from django.urls import path, include
from .views import HomeView, CategoryListView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/', CategoryListView.as_view(), name="category_list"),
]
