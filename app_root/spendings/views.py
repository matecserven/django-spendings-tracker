from rest_framework import viewsets
from .serializers import SpendingSerializer
from .models import SpendingORM


class SpendingViewSet(viewsets.ModelViewSet):
    queryset = SpendingORM.objects.all()
    serializer_class = SpendingSerializer
