from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import Subtitle
from .serializers import SubtitleSerializer

class SubtitleViewSet(viewsets.ModelViewSet):
    queryset = Subtitle.objects.all()
    serializer_class = SubtitleSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        phrase = request.query_params.get('phrase', '')
        if phrase:
            search_query = SearchQuery(phrase)
            results = Subtitle.objects.annotate(
                rank=SearchRank('search_vector', search_query)
            ).filter(search_vector=search_query).order_by('-rank')
            serializer = self.get_serializer(results, many=True)
            return Response(serializer.data)
        return Response({"detail": "Phrase query parameter is required."}, status=400)
