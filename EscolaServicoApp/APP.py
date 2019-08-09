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
DATABASE_NAME = 'escola_2.db'

# Recurso
@app.route("/enderecos", methods=['GET'])
def getEnderecos():
    logger.info("Listando endereços.")
    enderecos = []
    try:
        # abrir conexão com o banco de dados.
        conn = sqlite3.connect(DATABASE_NAME)
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

def dict_factory(linha, cursor):
    dicionario = {}
    for idx, col in enumerate(cursor.description):
        dicionario[col[0]] = linha[idx]
    return dicionario

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
