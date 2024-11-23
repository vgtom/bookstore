from flask import Flask
from api.routes import api
from database.db import db_session

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api/v1')
    
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000) 