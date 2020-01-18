from django.urls import path
from . import views

app_name ='to_do'

urlpatterns = [
    path('', views.add_to_do, name='add_to_do'),
    path('your_list/', views.ToDoList.as_view(), name='to_do_list'),
    path('true/<slug>', views.status_true, name='true'),
    path('false/<slug>', views.status_false, name='false'),
    path('delete/<slug>', views.Delete.as_view(), name='delete'),
    path('update/<slug>', views.update, name='update'),
    path('<username>/<slug>', views.detail_view, name='detail'),
]
