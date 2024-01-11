import os

from flask import Flask 

from .extensions import db
from .routes import main

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # postgres://prettyprinted_render_example_user:11vq6k72GmFJazhVpz3pFUko50djVZT1@dpg-ceukdhmn6mpglqdb4avg-a.oregon-postgres.render.com/prettyprinted_render_example
    #postgres://my_demo_db_98nb_user:WQAFv6317Di1rgb8WQoyO7QRyrpLITr6@dpg-cmg068mn7f5s73cair20-a.ohio-postgres.render.com/my_demo_db_98nb
    db.init_app(app)

    app.register_blueprint(main)

    return app