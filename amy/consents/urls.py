from django.urls import path, include

from consents import views

urlpatterns = [
    path('consents/', include([
        path('edit', views.ConsentsUpdate.as_view(), name='consents_edit'),
    ])),
]
