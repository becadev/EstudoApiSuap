# choices.py

TIPO_DE_AUXILIO = [
    ("auxilio transporte", "Auxílio transporte"),
    ("auxilio moradia", "Auxílio moradia"),
    ("alimentação estudantil", "Alimentação estudantil"),
    ("apoio a formação estudantil", "Apoio a formação estudantil"),
    ("auxilios eventuais", "Auxílios eventuais"),
    ("Outros", "Outros")
]

TIPO_DE_CHAMADO_CHOICES = [
    ("Alteração de documentos", "alteracao de documentos"),
    ("Arquivos pendentes", "arquivos pendentes"),
    ("Justificação", "justificacao"),
    ("Outro", "outro")
]

SOLICITADOS_CHOICES = [
    ("Todos", "todos"),
    ("Todos inscritos no programa", "todos inscritos no programa"),
    ("Selecionar alunos", "selecionar alunos")
]

TIPO_PERGUNTA_CHOICES = [
    ('paragrafo', 'Parágrafo'),
    ('multipla_escolha', 'Múltipla escolha'),
    ('caixa_selecao', 'Caixas de seleção')
]

TIPO_DOCUMENTO_CHOICES = [
    ("RG", "rg"),
    ("CPF", "cpf"),
    ("Comprovante de residência", "comprovante de residencia"),
    ("Histórico escolar", "historico escolar"),
    ("Comprovante de renda", "comprovante de renda"),
    ("Comprovante de ausência de renda", "comprovante de ausencia de renda"),
    ("Outros", "outros")
]

STATUS_PERGUNTA_CHOICES = [
    ("Respondida", "respondida"),
    ("Não respondida", "nao respondida")
]

STATUS_NOTIFICACAO_CHOICES = [
    ("Enviada", "enviada"),
    ("Não lida", "nao lida"),
    ("Lida", "lida")
]

CURSOS_IFRN_NATAL_CENTRAL = [
    # Técnico Integrado (Ensino Médio) – 9 cursos
    ("Administração", "administração"),                              
    ("Controle Ambiental", "controle ambiental"),                      
    ("Edificações", "edificações"),                               
    ("Eletrotécnica", "eletrotécnica"),                             
    ("Geologia", "geologia"),                                           
    ("Informática para Internet", "informática para internet"),         
    ("Manutenção e Suporte em Informática", "manutenção e suporte"),   
    ("Mecânica", "mecânica"),                                            
    ("Mineração", "mineração"),                                          

    # Técnico Subsequente – 12 cursos
    ("Controle Ambiental (Subsequente)", "controle ambiental subsequente"),         
    ("Edificações (Subsequente)", "edificações subsequente"),                     
    ("Eletrotécnica (Subsequente)", "eletrotécnica subsequente"),                
    ("Geologia (Subsequente)", "geologia subsequente"),                            
    ("Mecânica (Subsequente)", "mecânica subsequente"),                         
    ("Mineração (Subsequente)", "mineração subsequente"),                          
    ("Petróleo e Gás (Subsequente)", "petróleo e gás subsequente"),                  
    ("Redes de Computadores (Subsequente)", "redes de computadores subsequente"),    
    ("Manutenção e Suporte em Informática (Subsequente)", "manutenção suporte subsequente"), 
    ("Informática (Subsequente)", "informática subsequente"),                       
    ("Segurança do Trabalho (Subsequente)", "segurança do trabalho subsequente"),   
    ("Estradas (Subsequente)", "estradas subsequente"),                             

    # Cursos FIC (conf. DIATINF)
    ("Implantação de Serviços VoIP (FIC)", "implantacao servicos voip fic"),
    ("Aplicador de Revestimento Cerâmico (FIC)", "aplicador revestimento ceramico fic"),
    ("Artesanato com Material Reciclável (FIC)", "artesanato material reciclavel fic"),


    # Graduação – Engenharias
    ("Engenharia Civil", "engenharia civil"),
    ("Engenharia de Energia", "engenharia de energia"),
    ("Engenharia Sanitária e Ambiental", "engenharia sanitária e ambiental"),

    # Graduação – Tecnologias (Tec. Superiores)
    ("Tecnologia em Análise e Desenvolvimento de Sistemas", "tecnologia ads"),
    ("Tecnologia em Comércio Exterior", "tecnologia comércio exterior"),
    ("Tecnologia em Gestão Pública", "tecnologia gestão pública"),
    ("Tecnologia em Redes de Computadores", "tecnologia redes de computadores"),

    # Pós‑Graduação – Especializações
    ("Especialização em Engenharia de Segurança do Trabalho", "esp segurança trabalho"),
    ("Especialização em Ensino de Geociências", "esp ensino geociências"),
    ("Especialização em Gestão Ambiental", "esp gestão ambiental"),

    # Pós‑Graduação – Mestrados
    ("Mestrado Profissional em Ensino de Física", "mestrado prof ensino física"),
    ("Mestrado Profissional em Uso Sustentável de Recursos Naturais", "mestrado prof recursos naturais"),

    # Pós‑Graduação – Doutorado
    ("Doutorado Acadêmico em Educação Profissional", "doutorado educação profissional"),

]

STATUS_SOLICITACAO_CHOICES = [
    ("em analise", "Em Análise"),
    ("deferido", "Deferido"),
    ("indeferido", "Indeferido"),
    ("deferido sem recurso", "Deferido sem recurso"),
]

STATUS_BENEFICIO_CHOICES = [
    ("ativo", "Ativo"),
    ("inativo", "Inativo")
]

CAMPUS_IFRN_CHOICES = [
    ("Apodi", "Apodi"),
    ("Caico", "Caicó"),
    ("Canguaretama", "Canguaretama"),
    ("CearaMirim", "Ceará-Mirim"),
    ("CurraisNovos", "Currais Novos"),
    ("Ipanguacu", "Ipanguaçu"),
    ("JoaoCamara", "João Câmara"),
    ("Jucurutu", "Jucurutu"),
    ("Lajes", "Lajes"),
    ("Macau", "Macau"),
    ("Mossoro", "Mossoró"),
    ("NatalCentral", "Natal-Central"),
    ("NatalCidadeAlta", "Natal-Cidade Alta"),
    ("NatalZonaNorte", "Natal-Zona Norte"),
    ("NovaCruz", "Nova Cruz"),
    ("Parelhas", "Parelhas"),
    ("Parnamirim", "Parnamirim"),
    ("PauDosFerros", "Pau dos Ferros"),
    ("SantaCruz", "Santa Cruz"),
    ("SaoGoncaloDoAmarante", "São Gonçalo do Amarante"),
    ("SaoPauloDoPotengi", "São Paulo do Potengi")
]