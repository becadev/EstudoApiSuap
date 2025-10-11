""" Services que irá realizar a requisição na api do SUAP para recuperar o token """
import requests
from rest_framework.response import Response
from rest_framework import status
from ..models import *

# Endpoint da api do SUAP
SUAP_TOKEN_URL = "https://suap.ifrn.edu.br/api/token/pair"
SUAP_MEUS_DADOS_URL = "https://suap.ifrn.edu.br/api/rh/meus-dados/"
SUAP_MEUS_DADOS_SEMESTRE = "https://suap.ifrn.edu.br/api/ensino/periodos"


class AutenticacaoSuap():

    # def __init__(self, matricula,senha):
    #     self.matricula
    #     self.autenticar_suap(matricula, senha)
    #     self.dados_aluno()
        
    def autenticar_suap(matricula, senha):
        """Função que realiza o login do SUAP e retorna o token"""
        dados_login = {"username": matricula, "password": senha}
        resposta_auth = requests.post(SUAP_TOKEN_URL, json=dados_login)

        if resposta_auth.status_code != 200:
            return None

        tokens = resposta_auth.json()
        token_access = tokens.get('access')
        
        headers = {
            'Authorization': f'Bearer {token_access}',
            'accept': 'application/json'
        }
        data = (requests.get(SUAP_MEUS_DADOS_URL, headers=headers)).json()
        periodo = (requests.get(SUAP_MEUS_DADOS_SEMESTRE, headers=headers)).json()
        
        return {
            "access": token_access,
            "refresh": tokens.get('refresh'),
            "headers": headers,
            "data" : data,
            "periodo": periodo
        }
    
    def dados_usuario(autenticacao, matricula):
        '''Função cria/salva dados do aluno no banco'''
        data = autenticacao["data"]
        refresh = autenticacao["refresh"]
        headers = autenticacao["headers"]
        access = autenticacao["access"]
        periodo = autenticacao["periodo"]
        nome = data.get("nome_usual")
        tipo_vinculo = data.get("tipo_vinculo")
        cpf = data.get("cpf")
        data = data.get("vinculo", {}) # dados mais detalhados estao dentro de vinculos no json 
       
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

        if "aluno" in tipo_vinculo.lower(): 
            Aluno.objects.update_or_create( #  update pq dados como status e periodos podem mudar 
                usuario = usuario,
                matricula = matricula,
                cpf = cpf,
                curso = data.get("curso"),
                status = data.get("situacao"),
                periodo = periodo.get("count"),
            )

            try:
                data = Aluno.objects.get(matricula = matricula)
            except Aluno.DoesNotExist:
                data = None

        if "assistente social" in tipo_vinculo.lower(): 
            AssistenteSocial.objects.update_or_create(
                usuario = usuario,
                matricula = matricula,
            )

            try:
                data = AssistenteSocial.objects.get(matricula = matricula)
            except Aluno.DoesNotExist:
                data = None

            

        
        