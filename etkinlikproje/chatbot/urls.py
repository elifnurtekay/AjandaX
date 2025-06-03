from django.urls import path
from .views import chat_api, chatbot_page

urlpatterns = [
    path('api/', chat_api, name="chat_api"),
    path('', chatbot_page, name="chatbot_page"),
]