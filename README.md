# 📧 User Log Mailer

This is a simple Python automation tool for Linux system administrators. It logs all *normal users* from `/etc/passwd`, collects their username, UID, and email (from the comment field), saves it to a log file, and sends it to a specified email address every month.

The script is scheduled to run using `cron` on the **20th of every month at 11:59 PM**.

---

## 📁 Project Structure

user-log-mailer/
├── cron/
│ └── user_log_mailer.cron 
├── logs/ 
├── scripts/
│ ├── generate_report.py 
│ └── email_config.py 
└── README.md


---

## ⚙️ Configuration

Edit `scripts/email_config.py` with your SMTP details:

EMAIL_FROM = "youremail@gmail.com"
EMAIL_TO = "destinationemail@gmail.com"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
USERNAME = "youremail@gmail.com"
PASSWORD = "your-app-password"


# Scheduling with Cron

The cron job is already defined in:
cron/user_log_mailer.cron

To install it:
crontab cron/user_log_mailer.cron

This will schedule the script to run every month on the 20th at 11:59 PM.



