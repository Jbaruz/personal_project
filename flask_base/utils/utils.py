from flask_base import mail
from flask_mail import Message

def enviar_email(message, email):

    msg = Message('Mensaje desde la web Recetas!', sender =  ('SISTEMA', 'no_responder@recetas.sa') , recipients = [email])
    msg.body = message
    msg.html = message
    mail.send(msg)
