from rest_framework import serializers
from apps.tag.models import Tag

class TagCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('id','fechaRegistro','fechaUpdate',)

class TagListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"