from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from .models import Career

class CareerSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()

    def get_id(self, career):
        return career.id

    def get_username(self, career):
        return career.username

    def get_created_datetime(self, career):
        return career.created_at

    def get_title(self, career):
        return career.title

    def get_content(self, career):
        return career.content

    def create(self, validated_data):
        return Career.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    
class CareerWriteSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()

    # def get_username(self, career):
    #     return career.username

    # def get_title(self, career):
    #     return career.title

    # def get_content(self, career):
    #     return career.content

    def create(self, validated_data):
        return Career.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance
    

class UpdateCareerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Career
        fields = ['title', 'content']
    title = serializers.CharField(max_length=100, required=False)
    content = serializers.CharField(max_length=255, required=False)

    def validate_title(self, title):
        if len(title) > 100:
            raise serializers.ValidationError({
                'title':
                    _('Title length cannot be greater than 100 characters.')
            })
        title = title.strip()
        return title

    def validate(self, data):
        return data

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)