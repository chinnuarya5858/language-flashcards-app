from rest_framework import serializers
from .models import Flashcard

class FlashcardSerializer(serializers.ModelSerializer):
    class Meta:
        model=Flashcard
        fields='__all__'
        read_only_fields=['user']