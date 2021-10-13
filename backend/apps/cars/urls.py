from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register(r'', viewsets.MarkViewSet, basename='marks')


urlpatterns = [
    # path('test/', TestAPIView.as_view()),
    # path('fields/<str:field>/', ProductFieldsView.as_view()),
    # path('brands/', viewsets.BrandList.as_view(methods), name='brands'),
    # path('years/<int:pk>/', viewsets.YearViewSet.as_view()), 
    # path('complectations/<int:pk>/', viewsets.ComplectationViewSet.as_view()),
    path('', include(router.urls)),
]
