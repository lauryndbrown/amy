from django.urls import path, include

from consents import views

urlpatterns = [
    path('consents/<int:person_id>/', include([
        path('add', views.ConsentUpdate.as_view(), name='consent_add'),
    ])),
]
