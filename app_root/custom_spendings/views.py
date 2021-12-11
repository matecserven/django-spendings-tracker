from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from .models import Spending
from .serializers import SpendingSerializer


@api_view(['GET', 'POST'])
def spending_list(request):
    if request.method == 'GET':
        currency = request.query_params.get('currency')
        if currency is not None:
            spendings_data = Spending.objects.filter(currency=currency)
        else:
            spendings_data = Spending.objects.all()
        spendings_serializer = SpendingSerializer(spendings_data, many=True)
        return JsonResponse({'spendings': spendings_serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        spending_data = JSONParser().parse(request)
        spending_serializer = SpendingSerializer(data=spending_data)
        if spending_serializer.is_valid():
            spending_serializer.save()
            return JsonResponse({'message': 'Spending has been saved'}, status=status.HTTP_201_CREATED)
        return JsonResponse(spending_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def spending_detail(request, spending_id):
    try:
        spending_data = Spending.objects.get(pk=spending_id)
    except Spending.DoesNotExist:
        return JsonResponse({'message': 'The spending does not exists'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        spending_serializer = SpendingSerializer(spending_data)
        return JsonResponse(spending_serializer.data)

    elif request.method == 'PUT':
        spending_data = JSONParser().parse(request)
        spending_serializer = SpendingSerializer(data=spending_data)
        if spending_serializer.is_valid():
            spending_serializer.save()
            return JsonResponse({'message': 'The spending has been updated'}, status=status.HTTP_200_OK)
        return JsonResponse(spending_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        spending_data.delete()
        return JsonResponse({'message': 'Spending has been deleted'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def spending_ordered_list(request, order):
    spending_data = Spending.objects.all().order_by('amount')

    if order == 'desc':
        spending_data = spending_data.reverse()

    spending_serializer = SpendingSerializer(spending_data, many=True)
    return JsonResponse({'spendings': spending_serializer.data}, status=status.HTTP_200_OK)
