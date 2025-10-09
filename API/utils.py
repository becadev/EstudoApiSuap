class Utilitaria:
    @staticmethod
    def formatar_cpf(cpf: str) -> str:
        """Formata o CPF para o padrão XXX.XXX.XXX-XX."""
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValueError("CPF deve conter 11 dígitos numéricos.")
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"