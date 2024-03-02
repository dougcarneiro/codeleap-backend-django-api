from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from django.db import transaction

from .models import Career
from .serializers import (CareerSerializer,
                          UpdateCareerSerializer,
                          CareerWriteSerializer)
                          
class CareerApiView(APIView, LimitOffsetPagination):
    permission_classes = []

    @action(methods=['get'], detail=False)
    def get(self, request):
        careers_query = Career.objects.all()

        filter_username = request.query_params.get('username')
        filter_title = request.query_params.get('title')

        if filter_username:
            careers_query = careers_query.filter(
                item__icontains=filter_username
            )
        if filter_title:
            careers_query = careers_query.filter(
                value__icontains=filter_title
            )


        ordering = request.query_params.get('ordering')
        if ordering in ['username', '-username',
                        'created_at', '-created_at']:
            careers_query = careers_query.order_by(ordering)
        else:
            careers_query = careers_query.order_by('-updated_at')

        results = self.paginate_queryset(
            careers_query, request, view=self)
        serializer = CareerSerializer(results, many=True)
        return self.get_paginated_response(serializer.data)
    
    
    @action(methods=['post'], detail=False)
    def post(self, request):
        data = {
            'username': request.data.get('username'),
            'title': request.data.get('title'),
            'content': request.data.get('content'),

        }
        item = Career(
            username=request.data.get('username'),
            title=request.data.get('title'),
            content=request.data.get('content'),
        )

        career_serializer = CareerWriteSerializer(
            instance=item, data=data, context=request)
        if not career_serializer.is_valid():
            return Response(career_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            new_career = career_serializer.save()
            new_career_serializer = CareerWriteSerializer(new_career)

        return Response(new_career_serializer.data,
                        status=status.HTTP_201_CREATED)
        

class CareerByIDApiView(APIView):
    permission_classes = []
    
    def get(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            career = Career.objects.get(id=id)
        except (Career.DoesNotExist, KeyError):
            return Response('Career not found',
                            status=status.HTTP_404_NOT_FOUND)

        serializer = CareerSerializer(career, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            career = Career.objects.get(id=id)
        except (Career.DoesNotExist, KeyError):
            return Response('Career not found',
                            status=status.HTTP_404_NOT_FOUND)

        data = {
            "title": request.data.get("title", career.title),
            "content": request.data.get("content", career.content),
        }

        update_serializer = UpdateCareerSerializer(
            instance=career, data=data)
        if not update_serializer.is_valid():
            return Response(update_serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        update_serializer.update(
            career, update_serializer.validated_data)
        return Response('Career updated.', status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        try:
            id = kwargs['id']
            career = Career.objects.get(id=id)
        except (Career.DoesNotExist, KeyError):
            return Response('Career not found',
                            status=status.HTTP_404_NOT_FOUND)
        career.delete()
        return Response('Career removed.', status=status.HTTP_200_OK)