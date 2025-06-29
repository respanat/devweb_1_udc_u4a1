from flask_mail import Mail, Message
from flask import current_app


class EmailService:
    def __init__(self, mail_instance: Mail):
        self.mail_instance = mail_instance

    def send_simple_mail(self, to_email: str, subject: str, body: str):
        sender = current_app.config.get('Actividad4 DevWeb2025', 'respanat@unicartagena.edu.co')
        
        msg = Message(subject, sender=sender, recipients=[to_email])
        msg.body = body

        try:
            self.mail_instance.send(msg)
            print(f"Correo enviado a {to_email} con asunto: {subject}")
        except Exception as e:
            print(f"Error al enviar correo a {to_email}: {e}")
