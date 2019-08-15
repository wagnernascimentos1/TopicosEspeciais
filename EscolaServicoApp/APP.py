from flask import Flask
from flask import request
from flask import jsonify
from flask_json_schema import JsonSchema, JsonValidationError
import sqlite3
import logging

# Inicializando a aplicação.
app = Flask(__name__)

# Logging
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler = logging.FileHandler("escolaapp.log")
handler.setFormatter(formatter)

logger = app.logger
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Validação
schema = JsonSchema()
schema.init_app(app)

# Banco de dados.
DATABASE_NAME = 'EscolaApp_versao2.db'

#Validação
schema = JsonSchema()
schema.init_app(app)

endereco_schema = {
    'required': ['logradouro', 'complemento',  'bairro', 'cep', 'numero'],
    'properties': {
        'logradouro': {'type': 'string'},
        'complemento': {'type': 'string'},
        'bairro': {'type': 'string'},
        'cep': {'type': 'string'},
        'numero': {'type': 'integer'}
    }
}

escola_schema = {
    'required': ['nome', 'fk_id_endereco', 'fk_id_campus'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_endereco': {'type': 'integer'},
        'fk_id_campus': {'type': 'integer'}
    }
}

aluno_schema = {
    'required': ['nome', 'matricula', 'cpf', 'nascimento', 'fk_id_endereco', 'fk_id_curso'],
    'properties': {
        'nome': {'type': 'string'},
        'matricula': {'type': 'string'},
        'cpf': {'type': 'string'},
        'nascimento': {'type': 'string'},
        'fk_id_endereco': {'type': 'integer'},
        'fk_id_curso': {'type': 'integer'}
    }
}

professor_schema = {
    'required': ['nome', 'fk_id_endereco'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_endereco': {'type': 'integer'}
    }
}

disciplina_schema = {
    'required': ['nome', 'fk_id_professor'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_professor': {'type': 'integer'}
    }
}

curso_schema = {
    'required': ['nome','fk_id_turno'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_turno': {'type': 'integer'}
    }
}

campus_schema = {
    'required': ['sigla','cidade'],
    'properties': {
        'sigla': {'type': 'string'},
        'cidade': {'type': 'string'}
    }
}

turma_schema = {
    'required': ['nome','fk_id_curso'],
    'properties': {
        'nome': {'type': 'string'},
        'fk_id_curso': {'type': 'integer'}
    }
}

turno_schema = {
    'required': ['nome'],
    'properties': {
        'nome': {'type': 'string'}
    }
}

# Recurso
@app.route("/enderecos", methods=['GET'])
def getEnderecos():
    logger.info("Listando endereços.")
    enderecos = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_endereco;
        """)
        # iterando os registros.
        for linha in cursor.fetchall():
            endereco = {
                "id_endereco":linha[0],
                "logradouro":linha[1],
                "complemento":linha[2],
                "bairro":linha[3],
                "cep":linha[4],
                "numero":linha[5]
            }
            enderecos.append(endereco)
        logger.info(enderecos)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela endereço.")

    return jsonify(enderecos)

@app.route("/enderecos/<int:id>", methods=['GET'])
def getEndereco(id):

    logger.info("Listando endereço por id: %s"%(id))
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_endereco WHERE id_endereco = ?;
    """, (id, ));

    linha = cursor.fetchone()
    endereco = {
        "id_endereco":linha[0],
        "logradouro":linha[1],
        "complemento":linha[2],
        "bairro":linha[3],
        "cep":linha[4],
        "numero":linha[5]
    }

    # fechar conexão.
    conn.close()
    return jsonify(endereco)

@app.route("/endereco", methods=['POST'])
def setEndereco():
    # Recuperando dados do JSON.
    enderecoJson = request.get_json()

    logradouro = enderecoJson['logradouro']
    complemento = enderecoJson['complemento']
    bairro = enderecoJson['bairro']
    cep = enderecoJson['cep']
    numero = enderecoJson['numero']

    # Inserir dados na Base.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_endereco(logradouro, complemento, bairro, cep, numero)
        VALUES(?, ?, ?, ?, ?);
    """, (logradouro, complemento, bairro, cep, numero))
    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    enderecoJson["id"] = id

    return jsonify(enderecoJson)

# Tabela Escola

@app.route("/escolas", methods=['GET'])
def getEscolas():
    logger.info("Listando escolas.")
    escolas = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_escola;
        """)
        # iterando os registros.
        for linha in cursor.fetchall():
            escola = {
                "nome":linha[0],
                "fk_id_endereco":linha[1],
                "fk_id_campus":linha[2],
            }
            escolas.append(escola)
        logger.info(escolas)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela escola.")

    return jsonify(escolas)

@app.route("/escolas/<int:id>", methods=['GET'])
def getEscola(id):
    logger.info("Listando escolas por id: %s"%(id))
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_escola WHERE id_escola = ?;
    """, (id, ));

    linha = cursor.fetchone()
    escola = {
        "nome":linha[0],
        "fk_id_endereco":linha[1],
        "fk_id_campus":linha[2],
    }

    # fechar conexão.
    conn.close()
    return jsonify(escola)

@app.route("/escola", methods=['POST'])
def setEscola():
    # Recuperando dados do JSON.
    escolaJson = request.get_json()

    nome = escolaJson['nome']
    fk_id_endereco = escolaJson['fk_id_endereco']
    fk_id_campus = escolaJson['fk_id_campus']

    # Inserir dados na Base.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_escola(nome, fk_id_endereco, fk_id_campus)
        VALUES(?, ?, ?);
    """, (nome, fk_id_endereco, fk_id_campus))

    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    escolaJson["id"] = id

    return jsonify(escolaJson)

# Tabela Campus

@app.route("/campi", methods=['GET'])
def getCampus():
    logger.info("Listando todos os campi.")
    campi = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_campus;
        """)
        for linha in cursor.fetchall():
            campus = {
                "id_campus":linha[0],
                "sigla":linha[1],
                "cidade":linha[2]
            }
            campi.append(campus)
        logger.info(campi)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela campus.")

    return jsonify(campi)

@app.route("/campus/<int:id>", methods=['GET'])
def getCampusById(id):
    logger.info("Listando campus por id: %s"%(id))
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_campus WHERE id_campus = ?;
    """, (id, ));

    linha = cursor.fetchone()
    campus = {
        "id_campus":linha[0],
        "sigla":linha[1],
        "cidade":linha[2]
    }

    # fechar conexão.
    conn.close()
    return jsonify(campus)

@app.route("/campus", methods=['POST'])
def setCampus():
    # Recuperando dados do JSON.
    campusJson = request.get_json()

    sigla = campusJson['sigla']
    cidade = campusJson['cidade']

    # Inserir dados na Base.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_campus(sigla, cidade)
        VALUES(?, ?);
    """, (sigla, cidade))
    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    campusJson["id"] = id

    return jsonify(campusJson)

# Tabela Aluno

@app.route("/alunos", methods=['GET'])
def getALunos():
    logger.info("Listando alunos.")
    alunos = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_aluno;
        """)
        # iterando os registros.
        for linha in cursor.fetchall():
            aluno = {
                "id_aluno":linha[0],
                "nome":linha[1],
                "matricula":linha[2],
                "cpf":linha[3],
                "nascimento":linha[4],
                "fk_id_endereco":linha[5],
                "fk_id_curso":linha[6],
            }
            alunos.append(aluno)
        logger.info(alunos)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela aluno.")

    return jsonify(alunos)

@app.route("/alunos/<int:id>", methods=['GET'])
def getAlunoById(id):
    logger.info("Listando alunos por id: %s"%(id))
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_aluno WHERE id_aluno = ?;
    """, (id, ));

    linha = cursor.fetchone()
    aluno = {
        "nome":linha[0],
        "matricula":linha[1],
        "cpf":linha[2],
        "nascimento":linha[3],
        "fk_id_endereco":linha[4],
        "fk_id_curso":linha[5]
    }

    # fechar conexão.
    conn.close()
    return jsonify(aluno)

@app.route("/aluno", methods=['POST'])
def setAluno():
    # Recuperando dados do JSON.
    alunoJson = request.get_json()

    nome = alunoJson['nome']
    matricula = alunoJson['matricula']
    cpf = alunoJson['cpf']
    nascimento = alunoJson['nascimento']
    fk_id_endereco = alunoJson['fk_id_endereco']
    fk_id_curso = alunoJson['fk_id_curso']

    # Inserir dados na Base.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_aluno(nome, matricula, cpf, nascimento, fk_id_endereco,fk_id_curso)
        VALUES(?, ?, ?, ?, ?, ?);
    """, (nome, matricula, cpf, nascimento, fk_id_endereco,fk_id_curso))

    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    alunoJson["id"] = id

    return jsonify(alunoJson)

# Tabela  curso

@app.route("/cursos", methods=['GET'])
def getCursos():
    logger.info("Listando todos os cursos.")
    cursos = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_curso;
        """)
        # iterando os registros.
        for linha in cursor.fetchall():
            curso = {
                "nome":linha[0],
                "turno":linha[1],
                "fk_id_turno":linha[2],
            }
            cursos.append(curso)
        logger.info(cursos)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela curso.")

    return jsonify(cursos)

@app.route("/cursos/<int:id>", methods=['GET'])
def getCursoById(id):
    logger.info("Listando cursos por id: %s"%(id))
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_curso WHERE id_curso = ?;
    """, (id, ));

    linha = cursor.fetchone()
    curso = {
        "nome":linha[0],
        "turno":linha[1],
        "fk_id_turno":linha[2],
    }

    # fechar conexão.
    conn.close()
    return jsonify(curso)

@app.route("/curso", methods=['POST'])
def setCurso():
    # Recuperando dados do JSON.
    cursoJson = request.get_json()

    nome = cursoJson['nome']
    turno = cursoJson['turno']
    fk_id_turno = cursoJson['fk_id_turno']

    # Inserir dados na Base.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_curso(nome, turno, fk_id_turno)
        VALUES(?, ?, ?);
    """, (nome, turno, fk_id_turno))

    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    cursoJson["id"] = id

    return jsonify(cursoJson)

# Tabela Turma

@app.route("/turmas", methods=['GET'])
def getTurmas():
    logger.info("Listando todas as turmas.")
    turmas = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_turma;
        """)
        # iterando os registros.
        for linha in cursor.fetchall():
            turma = {
                "id_turma":linha[0],
                "nome":linha[1],
                "fk_id_curso":linha[2],
            }
            turmas.append(turma)
        logger.info(turmas)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela turma.")

    return jsonify(turma)

@app.route("/turmas/<int:id>", methods=['GET'])
def getTurmaById(id):

    logger.info("Listando turma por id: %s"%(id))
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_turma WHERE id_turma = ?;
    """, (id, ));

    linha = cursor.fetchone()
    turma = {
        "id_turma":linha[0],
        "nome":linha[1],
        "fk_id_curso":linha[2],
    }

    # fechar conexão.
    conn.close()
    return jsonify(turma)

@app.route("/turma", methods=['POST'])
def setTurma():
    # Recuperando dados do JSON.
    turmaJson = request.get_json()

    nome = turmaJson['nome']
    fk_id_curso = turmaJson['fk_id_curso']

    # Inserir dados na Base.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_turma(nome, fk_id_curso)
        VALUES(?, ?);
    """, (nome, fk_id_curso))
    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    turmaJson["id"] = id

    return jsonify(turmaJson)

# Tabela Turno

@app.route("/turnos", methods=['GET'])
def getTurnos():
    logger.info("Listando todos os turnos.")
    turnos = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_turno;
        """)
        # iterando os registros.
        for linha in cursor.fetchall():
            turno = {
                "id_turno":linha[0],
                "nome":linha[1],
            }
            turnos.append(turno)
        logger.info(turnos)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela professor.")

    return jsonify(turnos)

@app.route("/turnos/<int:id>", methods=['GET'])
def getTurnoById(id):

    logger.info("Listando endereço por id: %s"%(id))
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_turno WHERE id_turno = ?;
    """, (id, ));

    linha = cursor.fetchone()
    turno = {
        "id_turno":linha[0],
        "nome":linha[1],
    }

    # fechar conexão.
    conn.close()
    return jsonify(turno)

@app.route("/turno", methods=['POST'])
def setTurno():
    # Recuperando dados do JSON.
    turnoJson = request.get_json()

    id_turno = turnoJson['id_turno']
    nome = turnoJson['nome']

    # Inserir dados na Base.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_turno(id_turno, nome)
        VALUES(?, ?);
    """, (id_turno, nome))
    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    turnoJson["id"] = id

    return jsonify(turnoJson)

# Tabela Professor

@app.route("/professores", methods=['GET'])
def getProfessores():
    logger.info("Listando todos os professores.")
    professores = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_professor;
        """)
        # iterando os registros.
        for linha in cursor.fetchall():
            professor = {
                "id_professor":linha[0],
                "nome":linha[1],
                "fk_id_endereco":linha[2],
            }
            professores.append(professor)
        logger.info(professores)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela professor.")

    return jsonify(professores)

@app.route("/professores/<int:id>", methods=['GET'])
def getProfessoresById(id):

    logger.info("Listando professor por id: %s"%(id))
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_professor WHERE id_professor = ?;
    """, (id, ));

    linha = cursor.fetchone()
    professor = {
        "id_professor":linha[0],
        "nome":linha[1],
        "fk_id_endereco":linha[2],
    }

    # fechar conexão.
    conn.close()
    return jsonify(professor)


@app.route("/professor", methods=['POST'])
def setProfessor():
    # Recuperando dados do JSON.
    professorJson = request.get_json()

    nome = professorJson['nome']
    fk_id_endereco = professorJson['fk_id_endereco']

    # Inserir dados na Base.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_professor(nome, fk_id_endereco)
        VALUES(?, ?);
    """, (nome, fk_id_endereco))
    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    professorJson["id"] = id

    return jsonify(professorJson)

@app.route("/disciplinas", methods=['GET'])
def getDisciplinas():
    logger.info("Listando as disciplinas.")
    disciplinas = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_disciplina;
        """)
        # iterando os registros.
        for linha in cursor.fetchall():
            disciplina = {
                "id_turma":linha[0],
                "nome":linha[1],
                "fk_id_professor":linha[2],
            }
            disciplinas.append(disciplina)
        logger.info(disciplinas)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela disciplina.")

    return jsonify(disciplinas)


@app.route("/disciplinas/<int:id>", methods=['GET'])
def getDisciplinaById(id):

    logger.info("Listando disciplina por id: %s"%(id))
    # abrir conexão com o banco de dados.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()

    # executar a consulta.​​
    cursor.execute("""
        SELECT * FROM tb_disciplina WHERE id_turma = ?;
    """, (id, ));

    linha = cursor.fetchone()
    disciplina = {
        "id_turma":linha[0],
        "nome":linha[1],
        "fk_id_professor":linha[2],
    }

    # fechar conexão.
    conn.close()
    return jsonify(disciplina)

@app.route("/disciplina", methods=['POST'])
def setDisciplina():
    # Recuperando dados do JSON.
    disciplinaJson = request.get_json()

    id_turma = disciplinaJson['id_turma']
    nome = disciplinaJson['nome']
    fk_id_professor = disciplinaJson['fk_id_professor']

    # Inserir dados na Base.
    conn = sqlite3.connect('EscolaApp_versao2.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_disciplina(id_turma, nome, fk_id_professor)
        VALUES(?, ?, ?);
    """, (id_turma, nome, fk_id_professor))
    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    disciplinaJson["id"] = id

    return jsonify(disciplinaJson)


# Mensagem de erro para recurso não encontrado.
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(JsonValidationError)
def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})


if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
