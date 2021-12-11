from rest_framework import serializers


from .models import SpendingORM


class SpendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpendingORM
        fields = ('id', 'amount', 'currency', 'description', 'date')
