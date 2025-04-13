from dotenv import load_dotenv
from christiangirls.config import Config
from flask import Flask
from flask_pagedown import PageDown
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import markdown

load_dotenv()



mail = Mail()

pagedown = PageDown()

db = SQLAlchemy()

crypt = Bcrypt()

angel = LoginManager()
angel.login_view = 'users.eden'

def LetThereBeLight(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    db.init_app(app)
    crypt.init_app(app)
    angel.init_app(app)
    pagedown.init_app(app)

    @app.template_filter('markdown')
    def render_markdown(text):
        return markdown.markdown(text, extensions=['extra', 'codehilite', 'nl2br'])

    from christiangirls.users.routes import users
    app.register_blueprint(users)

    from christiangirls.posts.routes import posts
    app.register_blueprint(posts)

    from christiangirls.main.routes import main
    app.register_blueprint(main)

    from christiangirls.errors.handlers import errors
    app.register_blueprint(errors)

    return app


