from app import config
from flask import Flask
from flask_login import LoginManager

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


app.config.from_object(config.LinuxDevelopmentConfig)
app.config.from_envvar('APP_SETTINGS', silent=True)

import views

