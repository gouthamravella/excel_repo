from rest_framework import serializers
from .models import Expressions

class ExpressionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expressions
        fields = '__all__'

class CauseAndEffectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expressions
        fields = ('id', 'domain', 'expression', 'intents')