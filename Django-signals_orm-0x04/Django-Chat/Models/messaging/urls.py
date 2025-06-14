from django.urls import path
from . import views


urlpatterns = [
    path('conversation/<int:conversation_id>/', views.conversation_detail),
    path('inbox/', views.inbox, name='inbox'),
]