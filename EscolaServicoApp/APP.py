from flask import Flask
import sqlite3
from flask import request
from flask import jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return ("Olá Mundo! Estou aprendendo Flask", 200)

# Inicio dos recursos da aplicação tb_escola

@app.route("/escolas", methods=['GET'])
def getEscolas():
    conn= sqlite3.connect('ifpb.db')
    cursor= conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_escola;
    """)
    escola = list ()
    for linha in cursor.fetchall():
        escola = {
            "id_escola": linha[0],
            "nome": linha[1],
            "logradouro": linha[2],
            "cidade": linha[3]
        }
        escolas.append(escola)
    conn.close()
    return jsonify(escolas)
    return ("Cadastrado com sucesso", 200)

@app.route("/escolas/<int:id>", methods=['GET'])
def getEscolasByID(id):
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_escola
        WHERE id_escola = ?;
    """, (id, ))

    for linha in cursor.fetchall():
        escola = {
        "id_escola": linha[0],
        "nome": linha[1],
        "logradouro": linha[2],
        "cidade": linha[3]
    }
    conn.close()
    return jsonify(linha)
    return ("Cadastrado com sucesso", 200)

@app.route("/escola", methods=['POST'])
def setEscola():
    print('Cadastrando a Escola')
    escola = request.get_json()
    nome = request.form["nome"]
    logradouro = request.form["logradouro"]
    cidade = request.form["cidade"]

    print(nome, logradouro, cidade)

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_escola(nome, cidade, logradouro)
        VALUES(?, ?, ?);
    """, (nome, cidade, logradouro))

    conn.commit()
    conn.close()
    id_escola = cursor.lastrowid
    tb_escola["id_escola"] = id_escola

    return jsonify(escola)
# Fim dos recursos da aplicação tb_escola

# Inicio dos recursos da aplicação tb_escola

@app.route("/alunos", methods=['GET'])
def getAlunos():
    conn= sqlite3.connect('ifpb.db')
    cursor= conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_aluno;
    """)
    alunos = ()

    for linha in cursor.fetchall():
        aluno = {
            "id_aluno":linha[0],
            "nome":linha[1],
            "matricula":linha[2],
            "cpf":linha[3],
            "nascimento":linha[4]
        }
        alunos.append(aluno)

    conn.close()

    return jsonify(alunos)
    return ("Cadastrado com sucesso", 200)


@app.route("/alunos/<int:id>", methods=['GET'])
def getAlunosByID(id):
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM tb_aluno where id=?;

    """,(id, ))

    linha = cursor.fetchone()
    tb_aluno = {
        "id_aluno":linha[0],
        "nome":linha[1],
        "matricula":linha[2],
        "cpf":linha[3],
        "nascimento":linha[4],
    }
    conn.close()
    return jsonify(linha)
    return ("Listado com sucesso", 200)

@app.route("/aluno", methods=['POST'])
def setAluno():
    print('Cadastrando o aluno')
    aluno = request.get_json()
    nome = aluno['nome']
    matricula = aluno['matricula']
    cpf = aluno['cpf']
    nascimento = aluno['nascimento']

    print(nome, matricula, cpf, nascimento)

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_aluno(nome, nascimento, matricula, cpf)
        VALUES(?, ?, ?, ?);
    """,(nome, nascimento, matricula, cpf))

    conn.commit()
    conn.close()

    id = cursor.lastrowid
    aluno["id_aluno"] = id

    return jsonify(aluno)
    return ("Aluno cadastrado com sucesso!", 200)

# Inicio dos recursos da aplicação tb_curso

@app.route("/cursos", methods=['GET'])
def getCursos():
    conn= sqlite3.connect('ifpb.db')
    cursor= conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_curso;
    """)
    for linha in cursor.fetchall():
        print(linha)
    conn.close()

    return ("Executado", 200)

@app.route("/cursos/<id>", methods=['GET'])
def getCursosByID(id):
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM tb_curso where id=?;

    """,id)
    conn.close()
    return ("Executado", 200)


@app.route("/curso", methods=['POST'])
def setCurso():
    print('Cadastrando o aluno no curso')
    nome = request.form["nome"]
    turno = request.form["turno"]

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_curso(nome, turno)
        VALUES(?, ?);
    """,(nome, turno))

    conn.commit()
    conn.close()

    return ('Curso cadastrado no curso com sucesso!', 200)

# Fim dos recursos da aplicação tb_escola

# Inicio dos recursos da aplicação tb_turma

@app.route("/turmas", methods=['GET'])
def getTurmas():
    conn= sqlite3.connect('ifpb.db')
    cursor= conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_turma;
    """)

    turmas = list()
    for linha in cursor.fetchall():
        turma = {
            "id_turma" : linha[0],
            "nome" : linha[1],
            "curso" : linha[2]
        }
        turmas.append(turma)

    conn.close()
    return jsonify(turmas)

    return ("Listado com sucesso", 200)


@app.route("/turmas/<id>", methods=['GET'])
def getTurmaByID(id):
    conn = sqlite3.connect('ifpb.# DEBUG: ')
    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM tb_turma where id=?;

    """,(id, ))
    linha = cursor.fetchone()
    turma = {
        "id_turma" : linha[0],
        "nome" : linha[1],
        "curso" : linha[2]
    }
    conn.close()

    return jsonify(linha)
    return ("Listado com sucesso", 200)

@app.route("/turma", methods=['POST'])
def setTurma():
    print('Cadastrando o aluno no curso')
    curso = request.get_json()
    nome = request.form["nome"]
    curso = request.form["curso"]

    print(nome, turno)

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_turma(nome, curso)
        VALUES(?, ?);
    """,(nome, curso))

    conn.commit()
    conn.close()

    id = cursor.lastrowid
    turma["id_turma"] = id

    return jsonify(curso)
    return ("Cadastro de Curso realizado com sucesso!", 200)

# Fim dos recursos da aplicação tb_turma

# Inicio Recursos da aplicação tb_disciplina

@app.route("/disciplinas", methods=['GET'])
def getDisciplinas():

    conn = sqlite3.connect(database)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM tb_disciplina;
    """)

    disciplinas = list()
    for linha in cursor.fetchall():
        disciplina = {
            "id_disciplina" : linha[0],
            "nome" : linha[1]
        }
        disciplinas.append(disciplina)
    conn.close()

    return jsonify(disciplinas)

    return ("Cadastrado com sucesso", 200)

@app.route("/disciplinas/int:id>", methods=['GET'])
def getDisciplinaByID(id):
    conn= sqlite3.connect('ifpb.db')
    cursor= conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_disciplina WHERE id_disciplina = ?;
    """, (id,))

    linha = cursor.fetchone()
    disciplina = {
        "id_disciplina" : linha[0],
        "nome" : linha[1]
    }
    conn.close()
    return jsonify(linha)
    return ("Cadastrado com sucesso", 200)

@app.route("/disciplina", methods=['POST'])
def setDisciplina():
    disciplina = request.get_json()
    nome = disciplina['nome']

    print(nome)

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_disciplina(nome)
        VALUES(?);
    """, (nome,))

    conn.commit()
    conn.close()

    id = cursor.lastrowid
    disciplina["id_disciplina"] = id

    return jsonify(disciplina)

    return ("Disciplina cadastrada com sucesso!", 200)
# Fim dos recursos da aplicação tb_disciplina

#INICIO DA IMPLEMENTAÇÃO DOS MÉTODOS PUT DAS TABELAS CRIADAS NO BANCO DE DADOS EscolaServicoApp.db

@app.route("/escola/<int:id>", methods=['PUT'])
def updateEscola(id):
    print ("Atualizando Escola")
    escola = request.get_json()
    nome = escola['nome']
    logradouro = escola['logradouro']
    cidade = escola['cidade']
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM tb_escola WHERE id_escola = ?; """, (id,))
    data = cursor.fetchone()
    if (data is not None):
        cursor.execute("""UPDATE tb_escola SET nome=?, logradouro=?, cidade=?""" (nome,logradouro, cidade, id))
        conn.commit()
    else:
        print ("Cadastrando Escola")
        cursor.execute(""" INSERT INTO tb_escola(nome, logradouro, cidade) VALUES(?,?,?); """, (nome,logradouro, cidade))
        conn.commit()
        id = cursor.lastrowid
        escola["id_escola"] = id
    conn.close()
    return jsonify(escola)
@app.route("/aluno/<int:id>", methods=['PUT'])
def updateAluno(id):
    print ("Atualizando Aluno")
    aluno = request.get_json()
    nome = aluno['nome']
    matricula = aluno['matricula']
    cpf = aluno['cpf']
    nascimento = aluno['nascimento']
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM tb_aluno WHERE id_aluno = ?; """, (id,))
    data = cursor.fetchone()
    if (data is not None):
        cursor.execute("""UPDATE tb_aluno SET nome=?, matricula=?, cpf=?,nascimento=? WHERE id_aluno = ? """, (nome, matricula, cpf, nascimento,id))
        conn.commit()
    else:
        print ("Cadastrando Aluno")
        cursor.execute(""" INSERT INTO tb_aluno(nome, matricula, cpf, nascimento) VALUES(?,?,?,?); """, (nome, matricula, cpf, nascimento))
        conn.commit()
        id = cursor.lastrowid
        aluno["id_aluno"] = id
    conn.close()
    return jsonify(aluno)
@app.route("/curso/<int:id>", methods=['PUT'])
def updateCurso(id):
    print ("Atualizando Curso")
    curso = request.get_json()
    nome = curso['nome']
    turno = curso['turno']
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM tb_curso WHERE id_curso = ?; """, (id,))
    data = cursor.fetchone()
    if (data is not None):
        cursor.execute("""UPDATE tb_curso SET nome=?, turno=? WHERE id_curso = ? """, (nome, turno, id))
        conn.commit()
    else:
        print ("Cadastrando Curso")
        cursor.execute(""" INSERT INTO tb_curso(nome, turno) VALUES(?,?); """, (nome, turno))
        conn.commit()
        id = cursor.lastrowid
        curso["id_curso"] = id
    conn.close()
    return jsonify(curso)
@app.route("/turma/<int:id>", methods=['PUT'])
def updateTurma(id):
    print ("Atualizando Turma")
    turma = request.get_json()
    nome = turma['nome']
    curso = turma['curso']
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM tb_turma WHERE id_turma = ?; """, (id,))
    data = cursor.fetchone()
    if (data is not None):
        cursor.execute(""" UPDATE tb_turma SET nome=?, curso=? WHERE id_disciplina = ?""", (nome,curso, id))
        conn.commit()
    else:
        print ("Cadastrando Turma")
        cursor.execute(""" INSERT INTO tb_turma(nome, curso) VALUES(?,?); """, (nome, curso))
        conn.commit()
        id = cursor.lastrowid
        turma["id_turma"] = id
    conn.close()
    return jsonify(turma)
@app.route("/disciplina/<int:id>", methods=['PUT'])
def updateDisciplina(id):
    print ("Atualizando Disciplina")
    disciplina = request.get_json()
    nome = disciplina['nome']
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute(""" SELECT * FROM tb_disciplina WHERE id_disciplina = ?; """, (id,))
    data = cursor.fetchone()
    if (data is not None):
        cursor.execute(""" UPDATE tb_disciplina SET nome=? WHERE id_disciplina = ?""", (nome, id))
        conn.commit()
    else:
        print ("Cadastrando Disciplina")
        cursor.execute(""" INSERT INTO tb_disciplina(nome) VALUES(?); """, (nome,))
        conn.commit()
        id = cursor.lastrowid
        disciplina["id_disciplina"] = id
    conn.close()
    return jsonify(disciplina)
#FIM DA IMPLEMENTAÇÃO DOS MÉTODOS PUT DAS TABELAS CRIADAS NO BANCO DE DADOS EscolaServicoApp.db

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug= True, use_reloader=True)
