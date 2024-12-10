from rest_framework import serializers
from store.models import Product, Category, BasketItem, Basket
import os
from users.serializers import UserSerializer


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializers(serializers.ModelSerializer):
    category = CategorySerializers()

    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializers(serializers.ModelSerializer):
    subcategory = SubCategorySerializers()
    photos = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('subcategory', 'slug', 'name', 'description', 'price', 'photos')

    def get_photos(self, obj):
        original_photo = obj.photo.url
        base_path, ext = os.path.splitext(obj.photo.name)
        small_photo = f"{base_path}_small{ext}"
        medium_photo = f"{base_path}_medium{ext}"
        return {
            'original': original_photo,
            'small': small_photo,
            'medium': medium_photo,
        }


class BasketItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_slug = serializers.SlugField(write_only=True)

    class Meta:
        model = BasketItem
        fields = ['product_slug', 'quantity', 'total_price', 'product_name', ]

    def create(self, validated_data):
        user = self.context['request'].user
        basket, created = Basket.objects.get_or_create(user=user)
        product_slug = validated_data.pop('product_slug')
        product = Product.objects.get(slug=product_slug)
        quantity = validated_data.get('quantity', 1)
        basket_item, item_created = BasketItem.objects.get_or_create(basket=basket, product=product)
        if not item_created:
            basket_item.quantity += quantity
        else:
            basket_item.quantity = quantity
        basket_item.save()

        return basket_item


class BasketSerializer(serializers.ModelSerializer):
    items = BasketItemSerializer(many=True, read_only=True, source='basketitem_set')
    user = UserSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Basket
        fields = ['user', 'items', 'total_price']

    def get_total_price(self, obj):
        return sum(item.total_price for item in obj.basketitem_set.all())
