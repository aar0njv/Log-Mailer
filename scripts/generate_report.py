#!/usr/bin/env python3

import subprocess
import datetime
import os
from email.message import EmailMessage
import smtplib

from email_config import EMAIL_FROM, EMAIL_TO, SMTP_SERVER, SMTP_PORT, USERNAME, PASSWORD

LOGS_DIR = os.path.join(os.path.dirname(__file__), '../logs/')
os.makedirs(LOGS_DIR, exist_ok=True)

def get_user():
    users = []

    try:
        command = "awk -F: '$3>=1000 && $1!=\"nobody\"{print$1, $3, $5}' /etc/passwd"
        result = subprocess.run(command, shell=True, text=True, capture_output=True,check=True)
        
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.strip().split(' ', 2)
                username = parts[0]
                uid = int(parts[1])
                email = parts[2] if len(parts)==3 else "No email"
                users.append((username,uid,email))

    except subprocess.CalledProcessError as e:
         print(f"Error running awk command: {e}")
    return users


def write_log(users):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = f'user_report_{timestamp}.log'
    log_path = os.path.join(LOGS_DIR, log_filename)

    with open(log_path, 'w') as f:
        for username, uid, email in users:
            f.write(f'Username: {username}\tUID: {uid}\tEmail: {email}\n')

    return log_path


def send_email(log_path):
    msg = EmailMessage()
    msg['Subject'] = "Monthly Users Report"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg.set_content("Attached is the monthly users report with UID and email info.")

    with open(log_path, 'r') as f:
        msg.add_attachment(f.read(), filename=os.path.basename(log_path))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout = 10) as server:
            server.starttls()
            server.login(USERNAME, PASSWORD)
            server.send_message(msg)

        print("Email sent successfully.")
    
    except Exception as e:
        print(f'Failed to send email: {e}')


def main():
    users = get_user()
    if users:
        log_path = write_log(users)
        send_email(log_path)
    else:
        print("No normal users found.")

if __name__ == '__main__':
    main()