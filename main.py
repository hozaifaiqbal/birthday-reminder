import pandas as pd
from datetime import datetime

data = pd.read_csv("birthdays.csv")

data.columns = data.columns.str.strip().str.lower()

print(data.columns)

today = datetime.now().strftime("%m-%d")

birthday_people = []

for index, row in data.iterrows():
    bday = datetime.strptime(row['birthday'], "%Y-%m-%d").strftime("%m-%d")
    
    if bday == today:
        birthday_people.append(row['name'])

print("Today's birthdays:", birthday_people)