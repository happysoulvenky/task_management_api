from .auth import auth_bp
from .main import main_bp
from .projects import project_bp
from .tasks import task_bp

def register_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
