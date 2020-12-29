from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from .serializers import PostSerializer, PreferenceSerializer
from .models import Post, Preference
from rest_framework.decorators import action
from django.db.models import Count
import datetime
import json

class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)

class PostViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=("post",), url_path="preference", detail=False)
    def preference(self, request, *args, **kwargs):
        serializer = PreferenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'preference set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

class AnalyticsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from_date = request.query_params.get('date_from')
        to_date = request.query_params.get('date_to')
        preference_records = Preference.objects.all()
        if from_date is None or to_date is None:
            obj = preference_records.extra({'dateonly': 'DATE(date)'}).values('dateonly', 'action').annotate(count = Count('action'))
        else:
            date_from = datetime.datetime.strptime(str(from_date), '%Y-%m-%d').date()
            date_to = (datetime.datetime.strptime(str(to_date), '%Y-%m-%d') + datetime.timedelta(days=1)).date()
            obj = preference_records.extra({'dateonly': 'DATE(date)'}).filter(date__range=(date_from, date_to)).values('dateonly', 'action').annotate(count = Count('action'))
        
        for actiondict in obj:
            if actiondict['action'] == 1:
                actiondict['action'] = 'like'
            else:
                actiondict['action'] = 'unlike'

        return Response(obj)