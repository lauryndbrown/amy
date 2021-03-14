from django.urls import path, include

from consents import views

urlpatterns = [
    path('consents/<int:person_id>/', include([
        path('add', views.ConsentUpdate.as_view(), name='consent_edit'),
        path('delete', views.ConsentDelete.as_view(), name='consent_delete'),
    ])),

]
