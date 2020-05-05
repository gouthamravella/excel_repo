from django.shortcuts import render
from django.db.models import Q
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

class ExpressionsListView(APIView):
    def get(self, request, format=None):
        domain = request.data.get('domain', '')
        try:
            expressions = Expressions.objects.filter(domain=domain)
            serializer = ExpressionsSerializer(expressions, many=True)
            return Response(data={'response':serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


class ExpressionsFilterView(APIView):
    def get(self, request, format=None):
        domain = request.data.get('domain', '')
        intents = request.data.get('intents', [])
        
        if domain is None or domain == '' or intents is None:
            return Response(data={'error':'Domain or Intents is empty'}, status=status.HTTP_400_BAD_REQUEST)
        if not len(intents):
            return Response(data={'error':'Intents list cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            causes_exprs = []
            effects_exprs = []
            for intent in intents:
                expression = Expressions.objects.filter(domain=domain, intents__contains=[intent])
                causes = [j for i in expression for j in i.cumulative_cause_intents] if len(expression) else []
                effects = [j for i in expression for j in i.cumulative_effect_intents] if len(expression) else []
                
                if causes:
                    for cause in causes:
                        exprs = Expressions.objects.filter(domain=domain, cumulative_cause_intents__contains=[cause])
                        causes_exprs.extend(exprs)
                if effects:
                    for effect in effects:
                        exprs = Expressions.objects.filter(domain=domain, cumulative_effect_intents__contains=[effect])
                        effects_exprs.extend(exprs)
            causes_serializer = ExpressionsSerializer(set(causes_exprs), many=True)
            effects_serializer = ExpressionsSerializer(set(effects_exprs), many=True)
            return Response(data={'response':{'causes':causes_serializer.data, 'effects':effects_serializer.data}}, status=status.HTTP_200_OK)
            # if serializer.is_valid(raise_exception=True):
        except Exception as e:
            return Response(data={'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)