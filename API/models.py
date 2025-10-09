from django.db import models 
from django.contrib.auth.models import AbstractUser 
from django.conf import settings 
from django.core.exceptions import ValidationError  
from .utils import Utilitaria
from django.utils import timezone 

from .choices import (
    TIPO_DE_AUXILIO,
    TIPO_DE_CHAMADO_CHOICES,
    SOLICITADOS_CHOICES,
    TIPO_PERGUNTA_CHOICES,
    TIPO_DOCUMENTO_CHOICES,
    STATUS_PERGUNTA_CHOICES,
    STATUS_NOTIFICACAO_CHOICES,
    CURSOS_IFRN_NATAL_CENTRAL,
    CAMPUS_IFRN_CHOICES, 
    STATUS_SOLICITACAO_CHOICES,
    STATUS_BENEFICIO_CHOICES
)

class Usuario(AbstractUser):
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")

    def __str__(self):
        return self.nome
    
    def clean(self):
        erros={}
        if len(self.username) < 3:
            erros['username']="O nome de usuário deve ter pelo menos 3 caracteres."
        if len(self.nome) < 10:
            erros['nome']="O nome completo deve ter pelo menos 10 caracteres."
        if erros:
            raise ValidationError(erros)
        
    @property
    def tipo(self):
        if hasattr(self, 'aluno'):
            return 'aluno'
        elif hasattr(self, 'assistentesocial'):
            return 'assistente_social'
        elif self.is_superuser:
            return 'admin'
        return 'desconhecido'

        
class Aluno(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    matricula = models.IntegerField(unique=True, verbose_name="Matrícula")
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF")
    curso = models.CharField(max_length=100, choices=CURSOS_IFRN_NATAL_CENTRAL, verbose_name="Curso")
    periodo = models.IntegerField(verbose_name="Período")
    status = models.CharField(max_length=100)

    def cpf_formatado(self):
        """Retorna o CPF formatado como XXX.XXX.XXX-XX."""
        if self.cpf:
            return Utilitaria.formatar_cpf(self.cpf)
        return self.cpf
    
    def __str__(self):
        return f"{self.usuario.nome} ({self.matricula})" if self.usuario else f"Aluno {self.matricula}"
    
    def clean(self):
        erros={}
        if self.matricula < 10**13:
            erros['matricula']="A matrícula do aluno deve ter no minímo 14 digitos."
        if self.periodo < 1:
            erros['periodo']="O período precisa ser acima de 1."
        if len(self.cpf) != 11 or not self.cpf.isdigit():
            erros['cpf']="O CPF deve ter 11 dígitos numéricos."
        if erros:
            raise ValidationError(erros)
        
class AssistenteSocial(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assistentesocial')
    matricula = models.IntegerField(unique=True, verbose_name="Matrícula")
    
    def __str__(self):
        return f"{self.usuario.nome} ({self.matricula})" if self.usuario else f"Assistente {self.matricula}"

    
    def clean(self):
        erros={}
        if self.matricula < 10**6:
            erros['matricula']="A matrícula da assistente social deve ter no minímo 7 digitos."
        if erros:
            raise ValidationError(erros)

class Chamado(models.Model):
    descricao = models.TextField()
    tipo_de_chamado = models.CharField(max_length=25, choices=TIPO_DE_CHAMADO_CHOICES, default="alteracao de documentos")
    tipo_de_auxilio = models.CharField(max_length=30, choices=TIPO_DE_AUXILIO, default="auxilio transporte")
    status = models.BooleanField()
    data_abertura = models.DateField(auto_now_add=True)
    data_analise = models.DateField(auto_now=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, verbose_name="chamados")
    assistente_social = models.ForeignKey(AssistenteSocial, on_delete=models.CASCADE, verbose_name="chamados") # não botei o on_delete na AS pra o chamado continuar se a AS for deletada
    
    def __str__(self):
        return f"{self.id} - {self.descricao} - {self.aluno}"
    
    def clean(self):
        erros = {}
        if self.descricao == "":
            erros['descricao'] = "O chamado deve ter uma descrição"
        if erros:
            raise ValidationError(erros) 
    
    class Meta:
        db_table = 'chamado'
         
class Formulario(models.Model):
    titulo = models.CharField(max_length=100)
    objetivo = models.TextField()
    tipo = models.CharField(max_length=30, choices=TIPO_DE_AUXILIO, default="auxilio transporte")
    solicitados = models.CharField(max_length=30, choices=SOLICITADOS_CHOICES, default="todos")
    data_inicio = models.DateField()
    data_fim = models.DateField()
    total_formulario = models.IntegerField() # total respondido?
    alunos_solicitados = models.IntegerField()
    sem_resposta = models.IntegerField()
    
    def __str__(self):
        return f"{self.titulo} - {self.objetivo}"
    
    def clean(self):
        erros = {}
        if self.titulo == "":
            erros['titulo'] = "O formulário deve ter um título"
        if self.data_fim < self.data_inicio:
            erros['data fim'] = "A data do fim  do formulário não pode ser menor que a data inicial"

        # if self.data_fim <= timezone.datetime.now().date:
        #     erros['data fim'] = "A data do fim do formulário pode ser posterior a hoje."
        
        if erros:
            raise ValidationError(erros)
        
    class Meta:
        db_table = 'formulario'
    
class FormularioQuestao(models.Model):
    formulario = models.ForeignKey('Formulario', on_delete=models.CASCADE, related_name='questoes')
    titulo_pergunta = models.CharField(max_length=250)
    tipo_pergunta = models.CharField(max_length=50, choices=TIPO_PERGUNTA_CHOICES, default='multipla escolha')
    obrigatoriedade = models.BooleanField()
    ordem = models.PositiveIntegerField(default=0) #para ordenar as questões no formulário
    
    class Meta:
        db_table = 'formulario_questao'
        ordering = ['ordem']
        
    def __str__(self):
        return f"{self.titulo_pergunta} ({self.get_tipo_pergunta_display()})"
    
    def clean(self):
        erros = {}
        if not self.titulo_pergunta or len(self.titulo_pergunta) < 5:
            erros['titulo_pergunta'] = "A pergunta deve ter um título com pelo menos 5 caracteres."
        if erros:
            raise ValidationError(erros)

class FormularioQuestaoOpcao(models.Model):
    questao = models.ForeignKey(FormularioQuestao, on_delete=models.CASCADE, related_name='opcoes')
    alternativa = models.CharField(max_length=250)

    class Meta:
        db_table = 'formulario_questao_opcao'
        ordering = ['id']

    def __str__(self):
        return f"{self.alternativa}"

    def clean(self):
        erros = {}
        if not self.alternativa or len(self.alternativa) < 1:
            erros['alternativa'] = "O enunciado da alternativa não pode estar vazio."
        #se a questao for de multipla escolha, deve ter opções
        if self.questao.tipo_pergunta in ['multipla escolha', 'caixas de selecao'] and not self.alternativa:
            erros['alternativa'] = "Questões de múltipla escolha devem ter alternativas definidas."
        if erros:
            raise ValidationError(erros)

class RespostaFormulario(models.Model):
    formulario = models.ForeignKey(Formulario, on_delete=models.CASCADE, related_name='respostas')
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    data_resposta = models.DateTimeField(auto_now_add=True)
    completo = models.BooleanField(default=False) #coloquei pra indicar se o formulário foi completamente respondido pelo aluno

    class Meta:
        db_table = 'resposta_formulario'
        unique_together = ('formulario', 'aluno') #um aluno só pode responder um formulário específico uma única vez 

    def __str__(self):
        return f"Resposta de {self.aluno} para {self.formulario}"

    def clean(self):
        erros = {}
        #verificação se o aluno está apto a responder o formulário
        if self.formulario.solicitados != 'todos' and self.aluno.curso not in self.formulario.solicitados:
            erros['aluno'] = "Este aluno não está no grupo solicitado para este formulário."
        if erros:
            raise ValidationError(erros)

class RespostaQuestao(models.Model):
    resposta_formulario = models.ForeignKey(RespostaFormulario, on_delete=models.CASCADE, related_name='respostas_questoes')
    questao = models.ForeignKey(FormularioQuestao, on_delete=models.CASCADE)
    opcao_escolhida = models.ForeignKey(FormularioQuestaoOpcao, on_delete=models.SET_NULL, null=True, blank=True)
    resposta_aberta = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'resposta_questao'
        unique_together = ('resposta_formulario', 'questao') #para evitar respostas duplicadas para mesma questao

    def __str__(self):
        return f"Resposta para {self.questao}"

    def clean(self):
        erros = {}
        #validação baseada no tipo de pergunta
        if self.questao.tipo_pergunta in ['texto', 'paragrafo'] and not self.resposta_aberta:
            erros['resposta_aberta'] = "Esta questão requer uma resposta textual."
            
        elif self.questao.tipo_pergunta in ['multipla escolha', 'caixas de selecao'] and not self.opcao_escolhida:
            erros['opcao_escolhida'] = "Esta questão requer uma seleção de opção."
        
        #validação da obrigatoriedade de resposta
        if self.questao.obrigatoriedade and not (self.opcao_escolhida or self.resposta_aberta):
            erros['opcao_escolhida'] = "Esta questão é obrigatória."
            erros['resposta_aberta'] = "Esta questão é obrigatória."
            
        if erros:
            raise ValidationError(erros)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
class Documento(models.Model):
    tipo_documento = models.CharField(max_length=35, choices=TIPO_DOCUMENTO_CHOICES)
    solicitacao = models.ForeignKey('Solicitacao', on_delete=models.CASCADE)  #rebeca   // # o cascade dleta as notificações se o usuário tbm for deletado, mas não sei se é uma boa opção usar, podem ter infos uteis msm que delete o usuário
    aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE) 

    class Meta:
        db_table = 'documento'

    def __str__(self):
        return f"Documento {self.id}"

class Pergunta(models.Model):
    enunciado = models.CharField(max_length=900)
    resposta = models.CharField(max_length=900, blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_PERGUNTA_CHOICES)
    data_realizacao = models.DateField(auto_now_add=True)
    data_resposta = models.DateField(null=True, blank=True)
    assistente_social = models.ForeignKey('AssistenteSocial', on_delete=models.SET_NULL, null=True, blank=True) 
    aluno = models.ForeignKey('Aluno', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'pergunta'

    def __str__(self):
        return f"Pergunta #{self.id}"

class Notificacao(models.Model): 
    titulo = models.CharField(max_length=25, null=True)
    data_envio = models.DateField(auto_now_add=True)
    mensagem = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_NOTIFICACAO_CHOICES)
    data_visualizacao = models.DateField(null=True, blank=True)
    usuario = models.ManyToManyField(Usuario, related_name="notificacoes")  

    class Meta:
        db_table = 'notificacao'

    def __str__(self):
        return f"Notificação #{self.id}" 
##coloquei o META pra ajudar os nomes das tabelas no banco fiquem iguaiss os que estão no dicionario de dadps, e coloquei o "def __str__(self):" pra ordenar e prdronizar melhor a exibção das notificações, por exemplo
##a quantidade de caracteres da matricula da assistente social é 7, e a quantidade de caracteres pra senha é 10, NO MÍNIMO.

class Solicitacao(models.Model):
    status = models.CharField(max_length=20, choices=STATUS_SOLICITACAO_CHOICES, default = "em analise")
    descricao = models.CharField(max_length=200)
    data_criacao = models.DateField(auto_now_add=True)
    data_deferimento = models.DateField(null= True, blank = True)
    id_assistente_social = models.ForeignKey('AssistenteSocial', on_delete=models.CASCADE, related_name="id_AS")
    id_aluno = models.ForeignKey('Aluno', on_delete=models.CASCADE, related_name="id_aluno")
    id_beneficio = models.ForeignKey('Beneficio', on_delete=models.CASCADE, related_name="id_beneficio")

    class Meta:
        db_table = "solicitacao"

    def clean(self):
        erros = {}        
        if self.data_criacao and self.data_deferimento and self.data_deferimento < self.data_criacao:
            erros['data_criacao'] = "Data de criação não pode ser maior que a Data de deferimento da solicitação"

        if self.status == 'deferido' and not self.data_deferimento:
            erros['data_deferimento'] = "Deferimento exige data de deferimento"

        if self.status == 'em analise' and self.data_deferimento:
            erros['status'] = "Status 'em análise' não deve ter data de deferimento"

        beneficio = self.id_beneficio 
        aluno = self.id_aluno

        # verificar se esse aluno já teve alguma solicitação 
        existe_deferimentos = Solicitacao.objects.filter(
            id_aluno=aluno,
            id_beneficio=beneficio,
            status='deferido'
        )
       
        # verifica se o beneficio desse aluno está ativo

        existe_deferimentos_ativo = Beneficio.objects.filter(
            id=beneficio.id,
            status='ativo'
        )
        
        if existe_deferimentos.exists() and existe_deferimentos_ativo.exists():
            erros['id_beneficio'] = "O aluno já possui uma solicitação deferida ativa para este benefício."
        
        if erros:
            raise ValidationError(erros)

    def __str__(self):
        return f"Solicitação {self.status}"


class Beneficio(models.Model):
    tipo_auxilio = models.CharField(max_length=100, choices = TIPO_DE_AUXILIO)
    status = models.CharField(max_length=50, choices = STATUS_BENEFICIO_CHOICES)
    data_inicio = models.DateField(auto_now_add=True)
    data_fim = models.DateField()
    id_auxilio = models.ForeignKey('Auxilio',on_delete=models.CASCADE, related_name="id_auxilio")

    def clean(self):
        erros = {}        
        if self.data_fim and self.data_inicio and self.data_inicio > self.data_fim:
            erros['data_inicio'] = "Data de criação não pode ser maior que a Data de deferimento da solicitação"
        if erros:
            raise ValidationError(erros)

    def __str__(self):
        return f"Benefício {self.tipo_auxilio} | {self.status}"
    
    class Meta:
        db_table = "beneficio"


class Auxilio(models.Model):
    campus = models.CharField(max_length=100, choices = CAMPUS_IFRN_CHOICES)
    qtd_participantes = models.IntegerField(blank=True, null=True)
    qtd_chamados = models.IntegerField(blank=True, null=True)
    impedir_aluno = models.BooleanField(default=False)
    exigir_comprov = models.BooleanField(default=False)
    exigir_frequen = models.BooleanField(default=False)
    disponibilidade = models.BooleanField(default=False)
    edital = models.CharField(max_length=100, blank=True, null=True)


    def __str__(self):
        return f"Auxilio {self.disponibilidade} do {self.campus} com total de {self.qtd_participantes} participantes"
    
    def clean(self):
        erros = {}
        if self.qtd_participantes < 0 :
            erros['qtd_participantes'] = "Quantidade de participantes não pode ser negativa"
        if self.qtd_chamados < 0:
            erros['qtd_chamados'] = "Quantidade de chamados não pode ser negativa"

        if self.disponibilidade :
            if not self.edital:
                erros['edital'] = "Auxílio disponível exige edital"
            if not self.exigir_frequen :
                erros['exigir_frequen'] = "Auxílio disponível exige frequência"
            if not self.exigir_comprov :
                erros['exigir_comprov'] = "Auxílio disponível exige comprovante"

        if not self.disponibilidade:
            if self.exigir_frequen :
                erros['exigir_frequen'] = "Auxílio indisponível não exige frequência"
            if self.exigir_comprov:
                erros['exigir_comprov'] = "Auxílio indisponível não exige comprovante"
            if  self.impedir_aluno:
                erros['impedir_aluno'] = "Auxílio indisponível não permite aluno solicitar"

        if erros:
            raise ValidationError(erros)

    class Meta:
        db_table = "auxilio"