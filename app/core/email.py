import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from typing import Optional

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_FROM
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))
    
    with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg)

def send_welcome_email(email: str, name: str):
    subject = "Welcome to Our Hiring Platform"
    body = f"""
    <html>
        <body>
            <h1>Welcome, {name}!</h1>
            <p>Your account has been successfully created.</p>
            <p>You can now log in and start applying for jobs.</p>
        </body>
    </html>
    """
    send_email(email, subject, body)

def send_password_reset_email(email: str, temp_password: str):
    subject = "Your Password Reset Request"
    body = f"""
    <html>
        <body>
            <h1>Password Reset</h1>
            <p>Your temporary password is: <strong>{temp_password}</strong></p>
            <p>Please log in and change your password immediately.</p>
        </body>
    </html>
    """
    send_email(email, subject, body)

def send_application_confirmation(email: str, job_title: str):
    subject = "Application Submitted Successfully"
    body = f"""
    <html>
        <body>
            <h1>Application Received</h1>
            <p>Your application for {job_title} has been submitted successfully.</p>
        </body>
    </html>
    """
    send_email(email, subject, body)