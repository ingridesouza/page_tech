from app.models.mensagem import Mensagem

class AdminService:
    @staticmethod
    def listar_mensagens():
        return Mensagem.query.all()