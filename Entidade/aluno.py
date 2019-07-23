class Aluno(object):
    """docstring for Aluno."""

    def __init__(self, id, nome, endereco, matricula, cpf, nascimento):
        super(Aluno, self).__init__()
        self.id = id
        self.nome = nome
        self.endereco = endereco
        self.matricula = matricula
        self.cpf = cpf
        self.nascimento = nascimento
