import stripe
from django.conf import settings
from decouple import config

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView
from django.http.response import JsonResponse
from django.views.generic.base import TemplateView
from .models import CardDetail
from .serializers import CardDetailSerializer, CardCreateSerializer

class HomePageView(TemplateView):
    template_name = 'home.html'

class PaymentSuccess(APIView):
    def get(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        data = stripe.checkout.Session.retrieve(
            request.GET.get('session_id')
            )
        return Response(data, status = status.HTTP_200_OK)

class CancelledView(APIView):
    def get(self, request):
        data = {
            "status":"Payment failed. if your money is deducted, please contact sales@chat360.io."
        }
        return Response(data, status = 200)

class StripeConfig(APIView):
    def get(self, request):
        return JsonResponse({'publicKey': settings.STRIPE_PUBLISHABLE_KEY}, safe= False, status = status.HTTP_200_OK)

class CardDetailView(APIView):
    def get(self, request):
        cards = CardDetail.objects.all() # TODO user = request.user
        serializer = CardDetailSerializer(cards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CardCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        card_detail = serializer.save()
        data = CardDetailSerializer(card_detail).data
        return Response(data, status=status.HTTP_201_CREATED)

class CardDetailRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = CardDetailSerializer
    queryset = CardDetail.objects
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

class CreateCheckoutSession(APIView):
    def get(self, request):
        domain_url = config('DOMAIN_URL')
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                client_reference_id='aabrakadabragiligilichhu', # TODO replace it with users's hash
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Chat360 integration',
                        'quantity': 1,
                        'currency': 'inr',
                        'amount': '100',
                    }
                ]
            )
            return Response({'sessionId': checkout_session['id']})
        except Exception as e:
            return Response({'error': str(e)})