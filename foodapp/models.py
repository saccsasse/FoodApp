from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from foodapp.managers import ItemManager
from django.utils import timezone


class Item(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user_name','item_price']), #Composite Indexes
        ]

    #insted of indexes in shell Item.objects.all() now we have names of objects
    def __str__(self):
        return self.item_name + ":" + str(self.item_price)

    @staticmethod
    def get_absolute_url(): #redirect after adding new item, work only with existing items
        return reverse('foodapp:index')

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()

    # model=Item, pk=item_id, fk=User
    user_name = models.ForeignKey(User, on_delete=models.CASCADE, default=1) #on_delete means when user is deleted the item they added is also deletes, default=1 means ME as an admin
    item_name = models.CharField(max_length=200, db_index=True) #CharField requires a max_length. db_index=True - INDEXING
    item_desc = models.CharField(max_length=500)
    item_price = models.DecimalField(max_digits=10, decimal_places=2, default=True)
    #item_image = models.URLField(max_length=500, default='https://static.vecteezy.com/system/resources/previews/057/769/953/non_2x/a-cute-cartoon-illustration-of-a-smiling-golden-food-item-png.png')
    item_image = models.ImageField(upload_to='item_images/', null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_deleted = models.BooleanField(default=False) #soft delete flag
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = ItemManager()
    all_objects = models.Manager()

class Category(models.Model):
    name = models.CharField(max_length=200)
    added_on = models.DateField(auto_now=True)
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(Item, related_name='orders')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"