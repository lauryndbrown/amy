from django.urls import path, include

from consents import views

urlpatterns = [
    path('', include([
        path('', views.AllTerms.as_view(), name='all_terms'),
        path('add/', views.TermCreate.as_view(), name='term_add'),
    ])),
    path('term/<int:term_id>/', include([
        path('', views.TermDetails.as_view(), name='term_details'),
        path('edit/', views.TermUpdate.as_view(), name='term_edit'),
        path('delete/', views.TermDelete.as_view(), name='term_delete'),
        path('consent/<int:person_id>/', include([
            path('add', views.ConsentUpdate.as_view(), name='consent_add'),
        ])),
    ])),
]
