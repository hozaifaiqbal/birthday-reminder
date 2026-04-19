import pandas as pd
from datetime import datetime
import smtplib

# 🔐 YOUR EMAIL DETAILS
MY_EMAIL = "hozaifaiqbal0853@gmail.com"
APP_PASSWORD = "ncwfkbcorbxvpago"

# 📂 Load CSV
data = pd.read_csv("birthdays.csv")

# Clean columns (safe)
data.columns = data.columns.str.strip().str.lower()

# 📅 Today's date
today = datetime.now().strftime("%m-%d")

birthday_people = []

# 🎂 Check birthdays
for index, row in data.iterrows():
    bday = datetime.strptime(row['birthday'], "%Y-%m-%d").strftime("%m-%d")
    
    if bday == today:
        birthday_people.append(row['name'])

# 📩 Send Email
if birthday_people:
    names = "\n".join(birthday_people)

    message = f"""Subject:  Birthday Reminder

Today's birthdays:
{names}

Go wish them! 
"""

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, APP_PASSWORD)
        connection.sendmail(MY_EMAIL, MY_EMAIL, message)

    print("✅ Email sent successfully!")
else:
    print("No birthdays today.")