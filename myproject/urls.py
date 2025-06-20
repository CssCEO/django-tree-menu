from django.contrib import admin
from django.urls import path
from tree_menu.views import menu_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', menu_view, name='menu_view'),
]