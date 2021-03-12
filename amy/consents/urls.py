from django.urls import path, include

from consents import views

urlpatterns = [
    path('consent/<int:person_id>/', include([
        path('add', views.ConsentUpdate.as_view(), name='consent_add'),
    ])),
    # path('term/<int:term_id>/', include([
    #     path('consent/<int:person_id>/', include([
    #         path('add', views.ConsentUpdate.as_view(), name='consent_add'),
    #     ])),
    # ])),
]
