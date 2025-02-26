from app.models.mensagem import Mensagem
from app import db

class ContatoService:
    @staticmethod
    def enviar_mensagem(nome, email, mensagem):
        nova_mensagem = Mensagem(nome=nome, email=email, mensagem=mensagem)
        db.session.add(nova_mensagem)
        db.session.commit()