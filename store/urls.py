from django.urls import path
from rest_framework.routers import DefaultRouter

from store.apps import StoreConfig
from store.views import CategoryListApiView, SubCategoryListApiView, ProductListApiView, BasketItemViewSet, \
    BasketViewSet, BasketDeleteApi, ClearBasketApi, BasketUpdateApi

app_name = StoreConfig.name

router = DefaultRouter()
router.register(r'basket-items', BasketItemViewSet, basename='basket-item')

urlpatterns = [
    path('category/', CategoryListApiView.as_view(), name='category'),
    path('sub/category/', SubCategoryListApiView.as_view(), name='subcategory'),
    path('product/', ProductListApiView.as_view(), name='product'),
    path('basket/', BasketViewSet.as_view({'get': 'list'}), name='basket-list'),
    path('basket_delete/<str:slug>/', BasketDeleteApi.as_view(), name='basket-delete'),
    path('basket/clear/', ClearBasketApi.as_view(), name='basket-clear'),
    path('basket/<str:product__slug>/', BasketUpdateApi.as_view(), name='basket-update')

]+router.urls