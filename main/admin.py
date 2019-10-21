from django.contrib import admin

from main.models import (
                        Product,
                        ProductImage,
                        ProductTag)

# Register your models here.
admin.site.register(Product)
admin.site.register(ProductTag)
admin.site.register(ProductImage)
