from rest_framework import serializers
from .models import User, Asset, CheckoutLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class AssetSerializer(serializers.ModelSerializer):
    tagNumber = serializers.CharField(source='tag_number', allow_null=True, required=False)

    class Meta:
        model = Asset
        fields = ['id', 'name', 'tagNumber', 'status']

class CheckoutLogSerializer(serializers.ModelSerializer):
    # This nests the full User and Asset JSON objects inside the log!
    user = UserSerializer(read_only=True)
    asset = AssetSerializer(read_only=True)

    checkoutDate = serializers.DateTimeField(source='checkout_date', read_only=True)
    returnDate = serializers.DateTimeField(source='return_date', allow_null=True, required=False)

    class Meta:
        model = CheckoutLog
        fields = ['id', 'user', 'asset', 'checkoutDate', 'returnDate', 'status']