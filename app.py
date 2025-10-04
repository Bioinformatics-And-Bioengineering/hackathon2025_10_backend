# app.py
from flask import Flask
from flask_cors import CORS
import os

from routes.entries_api import entries_bp
from routes.goals_api import goals_bp
from routes.misc_api import misc_bp
from routes.image_api import image_bp
from routes.state_api import state_bp

def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False
    CORS(app, origins=os.getenv("CORS_ORIGINS", "*").split(","))

    app.register_blueprint(entries_bp, url_prefix="/api")
    app.register_blueprint(goals_bp,   url_prefix="/api")
    app.register_blueprint(misc_bp,    url_prefix="/api")
    app.register_blueprint(image_bp,   url_prefix="/api")
    app.register_blueprint(state_bp,   url_prefix="/api")

    @app.get("/healthz")
    def healthz():
        return {"ok": True}, 200

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT","5000")))
