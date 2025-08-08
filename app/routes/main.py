# app/routes/main.py
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/ping', methods=['GET'])
def ping():
    return {'message': 'pong'}
