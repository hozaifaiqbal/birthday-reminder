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
if birthday_people:
    names = "\n".join(birthday_people)

    message = f"""Subject: Birthday Reminder

Today's birthdays:
{names}

Go wish them!
"""

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(MY_EMAIL, APP_PASSWORD)
        connection.sendmail(MY_EMAIL, MY_EMAIL, message)

    print("✅ Email sent!")
else:
    print("No birthdays today.")