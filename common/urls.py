from django.urls import path

from common.views import IndexView, LogAPIView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/', IndexView.as_view()),
    path('api/logs/', LogAPIView.as_view(), name='log-api'),
]
