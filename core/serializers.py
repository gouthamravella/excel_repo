from rest_framework import serializers
from .models import Expressions

class ExpressionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expressions
        fields = '__all__'