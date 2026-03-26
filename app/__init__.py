import os
from flask import Flask, json, render_template

from app.webhook.routes import webhook
from app.events.routes import events
from app.extensions import mongo
from dotenv import load_dotenv

load_dotenv()

def create_app():
    # Get the root directory (parent of app folder)
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_dir = os.path.join(root_dir, 'app', 'templates')
    static_dir = os.path.join(root_dir, 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI")
    print(os.getenv("MONGO_URI"))
    mongo.init_app(app)

    app.register_blueprint(webhook)
    app.register_blueprint(events)
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app
