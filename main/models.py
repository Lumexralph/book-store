from django.db import models


class ActiveManager(models.Manager):
    def active(self):
        return self.filter(active=True)


class ProductTag(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        """return the tag natural key. In our case, we will use
         the slug as a natural key. The rationale behind this is
         that slugs, used as part of URLs, are unlikely to change
        """
        return (self.slug,)


class Product(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    slug = models.SlugField(max_length=48)
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(ProductTag, blank=True,
                                  related_name='products')

    objects = ActiveManager()

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='image')
    image = models.ImageField(upload_to='product-images')
    thumbnail = models.ImageField(upload_to='product-thumbnails', null=True)

    def __str__(self):
        return self.product.name
