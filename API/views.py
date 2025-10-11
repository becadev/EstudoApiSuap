from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import *
from .services.suap_auth import AutenticacaoSuap
from rest_framework.response import Response
from rest_framework import status
from .models import *
from drf_yasg.utils import swagger_auto_schema 

# APIVIEW nao precisa de serializer_class pq é instaciado dentro do proprio metodo, mas ele é usado com o swagger 
# e o retorno para o front é passado como json automaticamente pelo metodo response

class LoginSuapView(APIView):
    serializer_class = LoginSuapSerializer

    # anotação para poder receber parametros no swaagger
    @swagger_auto_schema(
        request_body=LoginSuapSerializer, 
        operation_summary="Autenticação de usuário via SUAP",
        operation_description="Recebe matrícula e senha para autenticar no SUAP e retornar um token de acesso."
    )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) # validacao do serializer

        matricula = serializer.validated_data['matricula']
        senha = serializer.validated_data['senha']

        if not matricula or not senha:
            return Response({"detail": "Credenciais inválidas."}, status=status.HTTP_400_BAD_REQUEST)


        autenticacao = AutenticacaoSuap.autenticar_suap(matricula, senha)
        data = AutenticacaoSuap.dados(autenticacao,matricula) # ainda não testei isso
        refresh = autenticacao["refresh"]
        headers = autenticacao["headers"]
        access = autenticacao["access"]
        
        if not data:
            return Response({"detail": "Usuário não encontrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            "access": access,
            "refresh": refresh,
            "headers": headers,
            "data" : data
        }, status=status.HTTP_200_OK)