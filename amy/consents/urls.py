from django.urls import path, include

from consents import views

urlpatterns = [
    # path('', views.dispatch, name='dispatch'),
    path('consents/edit/', views.ConsentsUpdate.as_view(), name='consents_edit'),
]
