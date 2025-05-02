import streamlit as st
import pandas as pd
import os

st.title("הגדרת עובדים – ניהול רשימת העובדים")

# מיקום הקובץ
file_path = "data/employees.csv"
os.makedirs("data", exist_ok=True)

# טופס להוספת עובד
with st.form("add_employee"):
    name = st.text_input("שם העובד")
    role = st.text_input("תפקיד")
    team = st.text_input("צוות")
    submitted = st.form_submit_button("הוסף עובד")

    if submitted:
        new_row = {"שם": name, "תפקיד": role, "צוות": team}
        df = pd.read_csv(file_path) if os.path.exists(file_path) else pd.DataFrame()
        df = df.append(new_row, ignore_index=True)
        df.to_csv(file_path, index=False)
        st.success("העובד נוסף בהצלחה")

# טבלת עובדים קיימים עם עריכה
if os.path.exists(file_path):
    st.subheader("רשימת עובדים קיימים")
    df = pd.read_csv(file_path)
    edited_df = st.data_editor(df, use_container_width=True, num_rows="dynamic")
    edited_df.to_csv(file_path, index=False)
    st.download_button("הורד כ-CSV", data=edited_df.to_csv(index=False).encode('utf-8'), file_name="employees.csv")
else:
    st.info("לא קיימים עובדים עדיין.")
