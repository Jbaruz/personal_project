from flask import Flask
from flask_mail import Mail
import os
UPLOAD_FOLDER = 'flask_base/static/uploads'
app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['MAIL_SERVER']='smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'd1c40c5d8dcc75'
app.config['MAIL_PASSWORD'] = os.environ.get("CLAVE_CORREO")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)