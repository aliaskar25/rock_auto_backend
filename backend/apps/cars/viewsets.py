from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import (
    Mark, Year, MarkModel, Complectation, Detail, SubDetail
)
from .serializers import (
    DetailListSerializer, MarkListSerializer, MarkYearSerializer, 
    YearSerializer, MarkModelSerializer,
    ComplectationSerializer, DetailSerializer, SubDetailSerializer
)


class MarkViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):
    queryset = Mark.objects.all()
    serializer_class = MarkListSerializer

    # def retrieve(self, request, *args, **kwargs):
    #     self.serializer_class = MarkYearSerializer
    #     return super().retrieve(request, *args, **kwargs)

    @action(detail=True, url_path='years')
    def get_years(self, request, pk=None):
        mark = Mark.objects.get(pk=pk)
        serializer = MarkYearSerializer(mark)
        return Response(serializer.data)

    @action(detail=True, url_path='models')
    def get_marks(self, request, pk=None):
        year_id = request.query_params['year_id']
        year = Year.objects.get(id=year_id)
        serializer = YearSerializer(year)
        return Response(serializer.data)

    @action(detail=True, url_path='complectations')
    def get_complectations(self, request, pk=None):
        model_id = request.query_params['model_id']
        model = MarkModel.objects.get(id=model_id)
        serializer = MarkModelSerializer(model)
        return Response(serializer.data)
    
    @action(detail=True, url_path='details')
    def get_details(self, request, pk=None):
        complectation_id = request.query_params['complectation_id']
        complectation = Complectation.objects.get(id=complectation_id)
        serializer = ComplectationSerializer(complectation)
        return Response(serializer.data)

    @action(detail=True, url_path='sub_details')
    def get_sub_details(self, request, pk=None):
        detail_id = request.query_params['detail_id']
        detail = Detail.objects.get(id=detail_id)
        serializer = DetailSerializer(detail)
        return Response(serializer.data)

    @action(detail=True, url_path='parts')
    def get_parts(self, request, pk=None):
        sub_detail_id = request.query_params['sub_detail_id']
        sub_detail = SubDetail.objects.get(id=sub_detail_id)
        serializer = SubDetailSerializer(sub_detail)
        return Response(serializer.data)
