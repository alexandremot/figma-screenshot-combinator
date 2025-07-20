from flask import Flask
from .config import DevConfig
from .adapters.assembly import Container
import os
import sys

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    if os.getenv('FLASK_ENV') == 'development':
        app.config.from_object(DevConfig())
    
    # Inicialize o container SEM passar app=app
    container = Container()
    
    # Configure o container para o app
    container.wire(modules=[__name__])
    
    from .blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
   
    return app
