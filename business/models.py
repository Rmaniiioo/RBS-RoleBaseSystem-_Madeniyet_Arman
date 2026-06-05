# from django.db import models
# from accounts.models import User

# # Create your models here.
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField(blank=True)

#     owner = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="products"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)


# class Shop(models.Model):
#     name = models.CharField(max_length=255)

#     owner = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="shops"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)


# class Order(models.Model):
#     number = models.CharField(max_length=50)

#     owner = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name="orders"
#     )

#     created_at = models.DateTimeField(auto_now_add=True)