from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Expressions
from .serializers import ExpressionsSerializer
# Create your views here.

class ExpressionsDetailView(APIView):
    def get(self, request, format=None):
        domain = request.data.get('domain', '')
        id = request.data.get('id', 0)
        try:
            expression = Expressions.objects.get(id=id, domain=domain)
            serializer = ExpressionsSerializer(data=expression)
            if serializer.is_valid(raise_exception=True):
                return Response(data={'response':serializer.data}, status=status.HTTP_200_OK)
        except Expressions.DoesNotExist as e:
            return Response(status=status.HTTP_204_NO_CONTENT)
        

class ExpressionsPostView(APIView):
    def post(self, request, format=None):
        domain = request.data.get('domain', '')
        expression = request.data.get('expression', '')
        intents = request.data.get('intents', [])
        cumulative_cause_intents = request.data.get('cumulative_cause_intents', [])
        cumulative_effect_intents = request.data.get('cumulative_effect_intents', [])
        
        if domain is None or expression is None or intents is None or cumulative_cause_intents is None or cumulative_effect_intents is None:
            return Response(data={'error':"Bad request"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            serializer = ExpressionsSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
            
            return Response(data={"response":"SUCCESS"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(data={"error":"{}".format(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

