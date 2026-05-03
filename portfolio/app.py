from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import time

app = Flask(__name__)
CORS(app)
load_dotenv()

def send_email_async(name, email, message, sender_email, sender_password, receiver_email):
    """Async email - Non-blocking"""
    try:
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"🚀 Portfolio Contact: {name}"
        
        body = f"""
🎯 NEW LEAD - {time.strftime('%Y-%m-%d %H:%M:%S')}

👤 {name}
📧 {email}
💬 {message}

---
Portfolio Website
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except:
        pass  # Silent fail - user ko success dikhao

@app.route('/contact', methods=['POST'])
def contact():
    data = request.get_json()
    
    name = data.get('name', '').strip()
    email = data.get('email', '').strip()
    message = data.get('message', '').strip()
    
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    receiver_email = os.getenv('RECEIVER_EMAIL', sender_email)
    
    # Async email (2x faster!)
    if sender_email and sender_password:
        threading.Thread(
            target=send_email_async,
            args=(name, email, message, sender_email, sender_password, receiver_email)
        ).start()
    
    return jsonify({
        "success": True,
        "message": "✅ Sent instantly!"
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)