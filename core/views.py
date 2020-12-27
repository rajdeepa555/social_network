from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from .serializers import PostSerializer, PreferenceSerializer
from .models import Post, Preference
from rest_framework.decorators import action


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
        preference_records = Preference.objects.all()
        content = {'message': 'Hello, Analytics!'}
        return Response(content)