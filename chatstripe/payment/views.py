from django.db.models import query
from rest_framework.views import APIView
from .models import CardDetail
from .serializers import CardDetailSerializer, CardCreateSerializer
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView


class CardDetailView(APIView):
    def get(self, request):
        cards = CardDetail.objects.all()
        serializer = CardDetailSerializer(cards, many=True)
        return Response({'status': True, 'data': serializer.data}, status=200)

    def post(self, request):
        serializer = CardCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card_detail = serializer.save()
        data = CardDetailSerializer(card_detail).data
        return Response({'status': True, 'data': data}, status=201)

class CardDetailRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = CardDetailSerializer
    queryset = CardDetail.objects
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
