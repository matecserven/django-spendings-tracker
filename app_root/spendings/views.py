from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import SpendingSerializer
from .models import SpendingORM


class SpendingViewSet(viewsets.ModelViewSet):
    queryset = SpendingORM.objects.all()
    serializer_class = SpendingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['currency']

    def get_queryset(self):
        queryset = self.queryset
        order = self.request.query_params.get('order')
        if order is not None:
            if order == 'asc':
                queryset = queryset.order_by('amount')
            elif order == 'desc':
                queryset = queryset.order_by('amount').reverse()
        return queryset
