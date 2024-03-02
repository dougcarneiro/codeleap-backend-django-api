from django.urls import path
from .views import (CareerApiView, CareerByIDApiView)


urlpatterns = [
    path('careers/', CareerApiView.as_view()),
    path('careers/<int:id>/', CareerByIDApiView.as_view())
]
