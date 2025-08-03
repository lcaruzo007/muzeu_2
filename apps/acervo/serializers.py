from rest_framework import serializers
from .models import ItemAcervo, CategoriaAcervo, FotoAcervo

class CategoriaAcervoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoriaAcervo
        fields = '__all__'

class FotoAcervoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FotoAcervo
        fields = '__all__'

class ItemAcervoSerializer(serializers.ModelSerializer):
    fotos = FotoAcervoSerializer(many=True, read_only=True)
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = ItemAcervo
        fields = '__all__'
