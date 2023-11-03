from flask import Flask, request, jsonify
from pymongo import MongoClient

client = MongoClient("mongodb+srv://dimensionalapp:js9w8QD1cSBQDOKY@cluster0.djri43u.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")
db = client["DimensionalApp"]
col_credenciais = db["credenciais"]

app = Flask(__name__)


@app.route("/ativacao", methods=["POST"])
def ativar_chave():
    payload = request.json

    if not (credencial := col_credenciais.find_one({"_id": payload["chave"]})):
        return jsonify({
            "success": False,
            "msg": "Chave não encontrada!"
        })

    if credencial["ativa"] and credencial["dispositivo"] == payload["dispositivo"]:
        return jsonify({
            "success": True,
            "msg": "Chave confirmada com sucesso!"
        })

    if credencial["ativa"] and credencial["dispositivo"] != payload["dispositivo"]:
        return jsonify({
            "success": False,
            "msg": "Essa chave já foi cadastrada em outro dispositivo"
        })

    col_credenciais.update_one(
        {"_id": payload["chave"]},
        {
            "$set": {
                "usuario": payload["usuario"],
                "ativa": True,
                "dispositivo": payload["dispositivo"],
                "data_ativacao": payload["dataAtivacao"]
            }
        }
    )

    return jsonify({
        "success": True,
        "msg": "Chave ativada com sucesso!"
    })


@app.route("/login", methods=["POST"])
def fazer_login():
    payload = request.json

    if not (usuario := col_credenciais.find_one({"usuario.login": payload["login"]})):
        return jsonify({
            "success": False,
            "msg": "Usuário não encontrado"
        })

    if usuario["usuario"]["senha"] != payload["senha"]:
        return jsonify({
            "success": False,
            "msg": "Senha incorreta!"
        })

    return jsonify({
        "success": True,
        "msg": "Logado com sucesso!"
    })


if __name__ == "__main__":
    app.run()
