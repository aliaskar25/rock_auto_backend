from rest_framework import serializers

from .models import (
    Mark, Year, MarkModel, Complectation, Detail, SubDetail
)


class MarkListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = ('id', 'name', )


class YearListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Year
        fields = ('id', 'year', )


class MarkYearSerializer(serializers.ModelSerializer):
    years = YearListSerializer(many=True)

    class Meta:
        model = Mark
        fields = ('id', 'name', 'years', )


class MarkModelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkModel
        fields = ('id', 'name')


class YearSerializer(serializers.ModelSerializer):
    mark_models = MarkModelListSerializer(many=True)
    
    class Meta:
        model = Year
        fields = ('id', 'year', 'mark_models', )


class ComplectationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complectation
        fields = ('id', 'name', )


class MarkModelSerializer(serializers.ModelSerializer):
    complectations = ComplectationListSerializer(many=True)
    
    class Meta:
        model = MarkModel
        fields = ('id', 'name', 'complectations', )


class DetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detail
        fields = ('id', 'name', )


class ComplectationSerializer(serializers.ModelSerializer):
    details = DetailListSerializer(many=True)

    class Meta:
        model = Complectation
        fields = ('id', 'name', 'details', )


class SubDetailListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubDetail
        fields = ('id', 'name', )
    

class DetailSerializer(serializers.ModelSerializer):
    sub_details = SubDetailListSerializer(many=True)
    
    class Meta:
        model = Detail
        fields = ('id', 'name', 'sub_details', )