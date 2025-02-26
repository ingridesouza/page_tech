from flask import Blueprint, render_template, request, jsonify
from app.services.contato_service import ContatoService

contato_bp = Blueprint('contato', __name__)

@contato_bp.route('/', methods=['GET'])
def index():
    return render_template('contato.html')

@contato_bp.route('/enviar-mensagem', methods=['POST'])
def enviar_mensagem():
    dados = request.form
    ContatoService.enviar_mensagem(dados['nome'], dados['email'], dados['mensagem'])
    return jsonify({"success": True})