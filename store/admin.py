from django.contrib import admin

from store.models import Category, SubCategory, Product, Basket, BasketItem


@admin.register(Category)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug',)


@admin.register(SubCategory)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'category',)


@admin.register(Product)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug', 'subcategory',)


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_email',)

    def user_email(self, obj):
        return obj.user.email


@admin.register(BasketItem)
class BasketItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product', 'quantity', 'total_price',)
