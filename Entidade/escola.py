class Escola(object):
    """docstring for Escola."""

    def __init__(self, id, nome, logradouro, cidade):
        super(Escola, self).__init__()
        self.id = id
        self.nome = nome
        self.logradouro = logradouro
        self.cidade = cidade
