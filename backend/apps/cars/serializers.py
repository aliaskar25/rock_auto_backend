from rest_framework import serializers

from .models import (
    Mark, Part, Year, MarkModel, Complectation, Detail, SubDetail,
    PartVariety, 
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


class PartVarietyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartVariety
        fields = ('id', 'name', 'price', )


class PartListSerializer(serializers.ModelSerializer):
    varieties = PartVarietyListSerializer(many=True)

    class Meta:
        model = Part
        fields = (
            'id', 'name', 'price', 'status', 'varieties', 'image', 
        )


class SubDetailSerializer(serializers.ModelSerializer):
    parts = PartListSerializer(many=True)

    class Meta:
        model = SubDetail
        fields = ('id', 'name', 'parts', )
