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
        VALUES(?, ?, ?, );
    """, (nome, fk_id_endereco, fk_id_campus))

    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    escolaJson["id"] = id

    return jsonify(escolaJson)

# Tabela Campus

@app.route("/campi", methods=['GET'])
def getCampi():
    logger.info("Listando os câmpus.")
    escolas = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect('EscolaApp_versao2.db')
        cursor = conn.cursor()
        # executar a consulta.​
        cursor.execute("""
            SELECT * FROM tb_campus;
        """)
        # iterando os registros.
        for linha in cursor.fetchall():
            campus = {
                "sigla":linha[0],
                "cidade":linha[1],
            }
            escolas.append(campus)
        logger.info(campi)
        # fechar conexão.
        conn.close()

    except(sqlite3.Error):
        logger.error("Aconteceu um erro com a tabela campus.")

    return jsonify(campus)

@app.route("/campi/<int:id>", methods=['GET'])
def getCampus(id):
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
        "sigla":linha[0],
        "cidade":linha[1],
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
        INSERT INTO tb_escola(sigla, cidade)
        VALUES(?, ?, );
    """, (sigla, cidade))
    conn.commit()
    conn.close()

    # Identificador do último registro inserido.
    id = cursor.lastrowid
    campusJson["id"] = id

    return jsonify(campusJson)


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

def validation_error(e):
    return jsonify({ 'error': e.message, 'errors': [validation_error.message for validation_error  in e.errors]})


if(__name__ == '__main__'):
    app.run(host='0.0.0.0', debug=True, use_reloader=True)
