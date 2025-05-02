import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

import gspread
from oauth2client.service_account import ServiceAccountCredentials

def send_to_google_sheets(row):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("gcreds.json", scope)
    client = gspread.authorize(creds)

    sheet_id = "ABC123XYZ456"  # שים כאן את המזהה שלך
    sheet = client.open_by_key(sheet_id).sheet1
    sheet.append_row(list(row.values()))

st.title("מסך ראש צוות – הזנת דיווחים")

file_path = "data/workers.csv"
os.makedirs("data", exist_ok=True)

# קריאת רשימת העובדים
employees_file = "data/employees.csv"
if os.path.exists(employees_file):
    employees_df = pd.read_csv(employees_file)
    employee_names = employees_df["שם"].tolist()
else:
    st.warning("לא קיימת רשימת עובדים. יש להגדיר במסך 'הגדרת עובדים'.")
    employee_names = []

with st.form("worker_form"):
    name = st.selectbox("בחר עובד", options=employee_names) if employee_names else st.text_input("שם העובד")
    role = st.text_input("תפקיד")
    project = st.text_input("פרויקט")
    date = st.date_input("תאריך", value=datetime.today())
    start_time = st.time_input("שעת התחלה")
    end_time = st.time_input("שעת סיום")
    submitted = st.form_submit_button("הוסף")

    if submitted:
        start = datetime.combine(date, start_time)
        end = datetime.combine(date, end_time)
        hours = round((end - start).seconds / 3600, 2)

        new_row = {
            "תאריך": date.strftime('%Y-%m-%d'),
            "שם": name,
            "תפקיד": role,
            "פרויקט": project,
            "שעת התחלה": start_time.strftime('%H:%M'),
            "שעת סיום": end_time.strftime('%H:%M'),
            "שעות עבודה": hours
        }

        df = pd.read_csv(file_path) if os.path.exists(file_path) else pd.DataFrame()
        df = df.append(new_row, ignore_index=True)
        df.to_csv(file_path, index=False)

        try:
            send_to_google_sheets(new_row)
            st.success("העובד נוסף ונשלח ל-Google Sheets")
        except Exception as e:
            st.warning(f"נוסף לקובץ מקומי אך נכשל בשליחה ל-Google Sheets: {e}")

st.subheader("עובדים שהוזנו להיום")
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    today = datetime.today().strftime('%Y-%m-%d')
    df_today = df[df["תאריך"] == today]
    st.dataframe(df_today, use_container_width=True)
else:
    st.info("אין נתונים עדיין.")
