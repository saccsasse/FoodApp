from rest_framework import serializers
from .models import Item, Order
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ItemSerializer(serializers.ModelSerializer):
    user_name = UserSerializer(read_only=True)
    class Meta:
        model = Item
        fields = ['id', 'user_name', 'item_name', 'item_desc', 'item_price', 'item_image']

    @staticmethod
    def validate_item_price(value):
        if value < 0:
            raise serializers.ValidationError('Item price cannot be negative')
        return value

    def validate(self, data):
        if data['item_name'].lower() == data['item_desc'].lower():
            raise serializers.ValidationError('Item description cannot be the same as the name')
        return data


class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True) #because items is another model not order
    user = serializers.StringRelatedField() #because items is another model not order
    class Meta:
        model = Order
        fields = ['id', 'user', 'created_at', 'items'] #id and created_at are only models that are in order model

