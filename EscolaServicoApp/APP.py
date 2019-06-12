from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route("/")
def hello_world():
    return ("Olá Mundo! Estou aprendendo Flask", 200)

@app.route("/escolas", methods=['GET'])
def getEscolas():
    conn= sqlite3.connect('ifpb.db')
    cursor= conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_escola;
    """)

    for linha in cursor.fetchall():
        print(linha)
    conn.close()

    return ("Executado", 200)

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
        print(linha)
    conn.close()

    return ("Executado", 200)

@app.route("/escola", methods=['POST'])
def setEscola():
    print('Cadastrando a escola')
    nome = request.form["nome"]
    logradouro = request.form["logradouro"]
    cidade = request.form["cidade"]

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_escola(nome, cidade, logradouro)
        VALUES(?, ?, ?);
    """, (nome, cidade, logradouro))

    conn.commit()
    conn.close()

    return ('Escola cadastrada com sucesso!', 200)

@app.route("/alunos", methods=['GET'])
def getAlunos():
    conn= sqlite3.connect('ifpb.db')
    cursor= conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_aluno;
    """)
    for linha in cursor.fetchall():
        print(linha)
    conn.close()

    return ("Executado", 200)


@app.route("/alunos/<int:id>", methods=['GET'])
def getAlunosByID(id):
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM tb_aluno where id=?;

    """,id)
    conn.close()
    return ("Executado", 200)


@app.route("/aluno", methods=['POST'])
def setAluno():
    print('Cadastrando o aluno')
    nome = request.form["nome"]
    nascimento = request.form["nascimento"]
    matricula = request.form["matricula"]
    cpf = request.form["cpf"]

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_aluno(nome, nascimento, matricula, cpf)
        VALUES(?, ?, ?, ?);
    """,(nome, nascimento, matricula, cpf))

    conn.commit()
    conn.close()

    return ('Aluno cadastrado com sucesso!', 200)

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


@app.route("/turmas", methods=['GET'])
def getTurmas():
    conn= sqlite3.connect('ifpb.db')
    cursor= conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_turma;
    """)
    for linha in cursor.fetchall():
        print(linha)
    conn.close()

    return ("Executado", 200)

@app.route("/turmas/<id>", methods=['GET'])
def getTurmaByID(id):
    conn = sqlite3.connect('ifpb.# DEBUG: ')
    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM tb_turma where id=?;

    """,id)
    conn.close()
    return ("Executado", 200)


@app.route("/turma", methods=['POST'])
def setTurma():
    print('Cadastrando o aluno no curso')
    nome = request.form["nome"]
    curso = request.form["curso"]

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tb_turma(nome, curso)
        VALUES(?, ?);
    """,(nome, curso))

    conn.commit()
    conn.close()

    return ('Turma cadastrada com sucesso!', 200)

@app.route("/disciplinas", methods=['GET'])
def getDisciplinas(id):
    conn = sqlite3.connect('ifpb.db')
    cursor = conn.cursor()

    cursor.execute("""

        SELECT * FROM tb_disciplina where id=?;

    """,id)
    conn.close()
    return ("Executado", 200)


@app.route("/disciplina", methods=['GET'])
def getDisciplina():
    conn= sqlite3.connect('ifpb.db')
    cursor= conn.cursor()
    cursor.execute("""
        SELECT *
        FROM tb_disciplina;
    """)
    for linha in cursor.fetchall():
        print(linha)
    conn.close()

    return ("Executado", 200)

@app.route("/disciplina", methods=['POST'])
def setDisciplina():
    print('Cadastrando disciplina')
    nome = request.form["nome"]

    conn = sqlite3.connect("ifpb.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tb_disciplina(nome)
        VALUES(?);
    """,(nome,)) # Tupla - estrutura de dado linear

    conn.commit()
    conn.close()

    return ('Disciplina cadastrada com sucesso!', 200)


if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
