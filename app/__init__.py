from flask import Flask
from flask_socketio import SocketIO
from dotenv import load_dotenv
import os

socketio = SocketIO(cors_allowed_origins="*", ping_timeout=30, ping_interval=10)

def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from .routes import bp
    app.register_blueprint(bp)

    socketio.init_app(app, async_mode='eventlet')
    return app
