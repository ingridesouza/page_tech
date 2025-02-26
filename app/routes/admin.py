from flask import Blueprint, render_template
from flask_login import login_required
from app.services.admin_service import AdminService

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/painel')
@login_required
def painel():
    mensagens = AdminService.listar_mensagens()
    return render_template('admin.html', mensagens=mensagens)