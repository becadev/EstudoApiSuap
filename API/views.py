from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import *
from .services.suap_auth import autenticar_suap
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

        autenticacao = autenticar_suap(matricula, senha)
        data = autenticacao["data"]
        refresh = autenticacao["refresh"]
        headers = autenticacao["headers"]
        access = autenticacao["access"]
        periodo = autenticacao["periodo"]
        nome = data.get("nome_usual")
        tipo_vinculo = data.get("tipo_vinculo")
        cpf = data.get("cpf")
        data = data.get("vinculo", {}) # dados mais detalhados estao dentro de vinculos no json 
        print(tipo_vinculo)

        if not autenticacao:
            return Response({"detail": "Falha de autenticação."}, status=status.HTTP_401_UNAUTHORIZED)
        # vai criar ou recuperar um usuario com o nome passado 
        usuario, created = Usuario.objects.get_or_create( # isso tem que mudar depois pq estou pegando o nome usual no suap e nao o nome completo
            nome = nome
        )

        if not usuario and created: # para caso seja criado um usuario no banco
            usuario = created

        print(f"""
        --- Aluno Info ---
            Matrícula: {matricula}
            CPF: {cpf}
            Curso: {data.get("curso")}
            Status: {data.get("situacao")}
            Período Atual: {periodo.get("count")}
            --------------------
            """
        )

        # isso aqui tem que ajeitar 
        # verifica se o aluno tem vinculo de aluno 
        # if "aluno" in tipo_vinculo.lower(): 
        #     print("is aluno")
        #     Aluno.objects.update_or_create( #  update pq dados como status e periodos podem mudar 
        #         usuario = usuario,
        #         defaults = {
        #             "matricula": matricula,
        #             "cpf": cpf,
        #             "curso": data.get("curso"),
        #             "status": data.get("situacao"),
        #             "periodo": periodo.get("count"),
        #         }
        #     )
        
        try:
            aluno = Aluno.objects.get(matricula = matricula)
        except Aluno.DoesNotExist:
            aluno = None
        
        return Response({
            "access": access,
            "refresh": refresh,
            "headers": headers,
            "usuario": AlunoSerializer(aluno).data if aluno else None,
            "matricula": matricula,
            "cpf": cpf,
            "curso": data.get("curso"),
            "status": data.get("situacao"),
            "periodo": periodo.get("count"),
            "tipo_usuario": tipo_vinculo
        }, status=status.HTTP_200_OK)