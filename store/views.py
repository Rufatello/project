from rest_framework import generics, viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from store.models import Category, SubCategory, Product, BasketItem, Basket
from store.pagination import MyPagination
from store.serializers import CategorySerializers, SubCategorySerializers, ProductSerializers, BasketItemSerializer, \
    BasketSerializer


class CategoryListApiView(generics.ListAPIView):
    'Просмотр все категорий'
    authentication_classes = [SessionAuthentication]
    pagination_class = MyPagination
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializers


class SubCategoryListApiView(generics.ListAPIView):
    'Просмотр подкатегорий'
    pagination_class = MyPagination
    serializer_class = SubCategorySerializers
    authentication_classes = [SessionAuthentication]
    queryset = SubCategory.objects.all().order_by('id')


class ProductListApiView(generics.ListAPIView):
    "просмотр всех продуктов"
    authentication_classes = [SessionAuthentication]
    pagination_class = MyPagination
    serializer_class = ProductSerializers
    queryset = Product.objects.all().order_by('id')


class BasketItemViewSet(viewsets.ModelViewSet):
    'добавление товара в корзину'
    queryset = BasketItem.objects.all()
    serializer_class = BasketItemSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BasketViewSet(viewsets.ViewSet):
    'просмотр корзины'
    def list(self, request):
        user = request.user
        basket, created = Basket.objects.get_or_create(user=user)
        serializer = BasketSerializer(basket)
        return Response(serializer.data)


class BasketDeleteApi(generics.DestroyAPIView):
    'удаление товара из корзины'
    serializer_class = BasketItemSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        product_slug = self.kwargs['slug']
        basket, _ = Basket.objects.get_or_create(user=user)

        try:
            basket_item = BasketItem.objects.get(basket=basket, product__slug=product_slug)
            return basket_item
        except BasketItem.DoesNotExist:
            raise NotFound("Нет такого товара")

    def delete(self, request, *args, **kwargs):
        basket_item = self.get_object()
        quantity_to_delete = int(request.data.get('quantity', basket_item.quantity))

        if quantity_to_delete > basket_item.quantity:
            return Response({"detail": "Недостаточно товаров в корзине."}, status=status.HTTP_400_BAD_REQUEST)

        basket_item.quantity -= quantity_to_delete
        if basket_item.quantity == 0:
            basket_item.delete()
        else:
            basket_item.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class ClearBasketApi(generics.DestroyAPIView):
    'очистка корзины'
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user = self.request.user
        basket, _ = Basket.objects.get_or_create(user=user)
        return basket

    def perform_destroy(self, basket):
        BasketItem.objects.filter(basket=basket).delete()


class BasketUpdateApi(generics.UpdateAPIView):
    'изменение количество товара в корзине'
    serializer_class = BasketItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'product__slug'
    def get_queryset(self):
        user = self.request.user
        return BasketItem.objects.filter(basket__user=user)

    def perform_update(self, serializer):
        quantity = serializer.validated_data['quantity']
        if quantity <= 0:
            serializer.instance.delete()
        else:
            serializer.save()
