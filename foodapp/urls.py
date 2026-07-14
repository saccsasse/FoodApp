from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = 'foodapp'
router = DefaultRouter()
router.register('items', views.ItemViewSet, basename='items')
router.register('orders', views.OrderViewSet, basename='orders')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include(router.urls)),
    # URL patterns of API built with Django Rest Framework (DRF)
    # path('api/items', views.ItemListCreateAPI.as_view(), name='item-list-api'),
    # path('api/items/<int:pk>', views.ItemRetrieveUpdateDestroyAPIView.as_view(), name='item-detail-api'),
    # URL patterns of Django App
    path('', views.index, name='index'),
    path('<int:id>/', views.detail, name='detail'), #dynamic ids that why it is in the brackets and with data type
    path('add/', views.create_item, name='create_item'),
    path('update/<int:pk>/', views.ItemUpdateView.as_view(), name='update_item'),
    path('delete/<int:pk>/', views.ItemDeleteView.as_view(), name='delete_item'),
]
