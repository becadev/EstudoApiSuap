""" Services que irá realizar a requisição na api do SUAP para recuperar o token """
import requests

# Endpoint da api do SUAP
SUAP_TOKEN_URL = "https://suap.ifrn.edu.br/api/token/pair"
SUAP_MEUS_DADOS_URL = "https://suap.ifrn.edu.br/api/rh/meus-dados/"
SUAP_MEUS_DADOS_SEMESTRE = "https://suap.ifrn.edu.br/api/ensino/periodos"

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