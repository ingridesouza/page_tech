from app.models.mensagem import Mensagem

class AuthService:
    @staticmethod
    def authenticate(username, password):
        # Lógica de autenticação (substitua por um sistema real)
        if username == "admin" and password == "senha123":
            return {"username": username}  # Simula um usuário
        return None