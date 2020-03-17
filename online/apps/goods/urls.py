from .views import GoodsListView
from django.urls import path

urlpatterns = [
    path('good', GoodsListView.as_view())
]