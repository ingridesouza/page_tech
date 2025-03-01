from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import bcrypt
from app.routes.admin import admin_bp  # Importar o Blueprint

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
app.secret_key = '927e3ae49c9827f64cb30496b705838b'  # Chave secreta para sessões

db = SQLAlchemy(app)

# Registrar o Blueprint (caso ainda queira ter admin em outra rota)
app.register_blueprint(admin_bp)

# Modelo da tabela de mensagens
class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)

# Modelo da tabela de usuários
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha_hash = db.Column(db.String(128), nullable=False)  # Armazena o hash da senha
    is_admin = db.Column(db.Boolean, default=False)

    def set_senha(self, senha):
        # Gera o hash da senha
        self.senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def verificar_senha(self, senha):
        # Verifica se a senha está correta
        return bcrypt.checkpw(senha.encode('utf-8'), self.senha_hash.encode('utf-8'))

# Cria o banco de dados (execute apenas uma vez)
with app.app_context():
    db.create_all()

# Cria um usuário administrador padrão (opcional, se quiser)
with app.app_context():
    if not Usuario.query.filter_by(email='admin@bytewave.com').first():
        admin = Usuario(email='admin@bytewave.com', is_admin=True)
        admin.set_senha('senha_segura')  # Define a senha com hash
        db.session.add(admin)
        db.session.commit()
        print("Usuário administrador padrão criado com sucesso!")

# Decorator para verificar autenticação via session
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rota para a página de login (GET)
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

# Rota para autenticar o usuário (POST)
@app.route('/login', methods=['POST'])
def autenticar():
    email = request.form.get('email')
    senha = request.form.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario and usuario.verificar_senha(senha):
        # Grava o ID do usuário na sessão
        session['usuario_id'] = usuario.id
        session['is_admin'] = usuario.is_admin

        # Se for admin, poderia ir para algum lugar especial se quisesse
        if usuario.is_admin:
            # Ainda existe esta rota mas não aparece no menu
            return redirect(url_for('admin.painel'))
        else:
            return redirect(url_for('index'))
    else:
        flash('Credenciais inválidas. Tente novamente.', 'error')
        return redirect(url_for('login'))

# Se quiser manter o painel de admin sem mostrar no menu
@app.route('/painel')
@login_required
def painel():
    if session.get('is_admin'):
        mensagens = Mensagem.query.all()
        return render_template('admin.html', mensagens=mensagens)
    else:
        flash('Acesso negado. Você não tem permissão para acessar esta página.', 'error')
        return redirect(url_for('index'))

# Rota para logout (não aparece no menu, mas você pode acessar via link direto)
@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado com sucesso.', 'success')
    return redirect(url_for('index'))

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

    nova_mensagem = Mensagem(nome=nome, email=email, mensagem=mensagem)
    db.session.add(nova_mensagem)
    db.session.commit()

    flash('Mensagem enviada com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
