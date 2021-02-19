# from . import views
# from django.urls import path
# from django.urls import path, re_path

# from .views import CreateChatView, ChatRoomView

# urlpatterns = [
#     path('', CreateChatView, name='index'),
#     path('<str:room_name>/', ChatRoomView, name='room'),
# ]


from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
