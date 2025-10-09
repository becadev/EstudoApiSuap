from rest_framework import serializers
from .models import *

class LoginSuapSerializer(serializers.Serializer):
    matricula = serializers.CharField(max_length=50, help_text="A matrícula do usuário no SUAP.")
    senha = serializers.CharField(max_length=128, style={'input_type': 'password'}, help_text="A senha do usuário no SUAP.")

    def validate_matricula(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("A matrícula deve conter apenas números.")
        
        if  7 > len(value) > 14 :
            raise serializers.ValidationError("Matrícula inválida")
        
        return value
    

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'


