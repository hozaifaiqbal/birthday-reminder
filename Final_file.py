import gspread
import pandas as pd
from datetime import datetime
import smtplib

# 🔐 Email
MY_EMAIL = "hozaifaiqbal0853@gmail.com"
APP_PASSWORD = "ncwfkbcorbxvpago"

# 🔗 Google Sheets
gc = gspread.service_account(filename="birthday-reminder.json")

sheet = gc.open("birthday_reminder").sheet1

data = sheet.get_all_records()
df = pd.DataFrame(data)

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# 📅 Today
today = datetime.now().strftime("%m-%d")

birthday_people = []

for index, row in df.iterrows():
    try:
        bday = datetime.strptime(row['birthday'], "%Y-%m-%d").strftime("%m-%d")
        
        if bday == today:
            birthday_people.append(row['name'])
    except:
        continue

# 📩 Email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

if birthday_people:
    names_html = "".join([f"<li>{name}</li>" for name in birthday_people])

    # 🎯 Subject
    subject = "🎉 Birthday Reminder - DON'T FORGET!"

    # 🎨 HTML Email Body
    html = f"""
    <html>
    <body style="font-family: Arial; background-color: #d3eef5; padding: 10px;">
        <div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px;">
            
            <h2 style="color: #ff4d4d;">🎂 Birthday Alert!</h2>
            
            <p style="font-size: 16px;">Today is the birthday of:</p>
            
            <ul style="font-size: 28px; color: #333;">
                {names_html}
            </ul>
            
            <p style="margin-top: 20px;">👉 Don’t forget to wish them!</p>
            
            <hr>
            <p style="font-size: 12px; color: gray;">Your Personal Reminder System</p>
        </div>
    </body>
    </html>
    """

    # 📩 Create message
    msg = MIMEMultipart()
    msg["From"] = MY_EMAIL
    msg["To"] = MY_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(html, "html"))

    # 📤 Send
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, APP_PASSWORD)
        connection.send_message(msg)

    print("✅ Beautiful email sent!")