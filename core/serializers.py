from rest_framework import fields, serializers
from .models import Post, Preference



class PostSerializer(serializers.ModelSerializer):
    """
    Serializer to save PostSerializer
    """
    class Meta:
        model = Post
        fields = ("id","title","content","author")

class PreferenceSerializer(serializers.ModelSerializer):
    """
    Serializer to save PreferenceSerializer
    """
    class Meta:
        model = Preference
        fields = "__all__"