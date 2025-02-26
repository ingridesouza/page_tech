from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.routes.admin import admin_bp

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
db = SQLAlchemy(app)

# Registrar o Blueprint do admin
app.register_blueprint(admin_bp)

# Modelo da tabela de mensagens
class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

# Cria o banco de dados (execute apenas uma vez)
with app.app_context():
    db.create_all()

# Rota para receber mensagens do formulário
@app.route('/enviar-mensagem', methods=['POST'])
def enviar_mensagem():
    dados = request.form
    nova_mensagem = Mensagem(nome=dados['nome'], email=dados['email'], mensagem=dados['mensagem'])
    db.session.add(nova_mensagem)
    db.session.commit()
    return jsonify({"success": True})

# Rota para o painel de administrador buscar mensagens
@app.route('/mensagens', methods=['GET'])
def listar_mensagens():
    mensagens = Mensagem.query.all()
    return jsonify([{"id": msg.id, "nome": msg.nome, "email": msg.email, "mensagem": msg.mensagem} for msg in mensagens])

# Rota principal
@app.route('/')
def index():
    return render_template('index.html')

# Rota para o formulário de contato
@app.route('/contato', methods=['GET'])
def mostrar_contato():
    return render_template('contato.html')

@app.route('/contato', methods=['POST'])
def contato():
    data = request.form
    nome = data.get("nome")
    email = data.get("email")
    mensagem = data.get("mensagem")
    
    print(f"Mensagem recebida: Nome: {nome}, Email: {email}, Mensagem: {mensagem}")
    return jsonify({"status": "success", "message": "Mensagem enviada com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)