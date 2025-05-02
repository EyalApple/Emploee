import streamlit as st
import pandas as pd
import os

st.title("מסך קשת – סיכום דיווחים")

file_path = "data/workers.csv"
if not os.path.exists(file_path):
    st.warning("אין נתונים זמינים עדיין.")
else:
    df = pd.read_csv(file_path)

    date_range = st.date_input("בחר טווח תאריכים", [])
    if len(date_range) == 2:
        start, end = [d.strftime('%Y-%m-%d') for d in date_range]
        df_filtered = df[(df["תאריך"] >= start) & (df["תאריך"] <= end)]
    else:
        df_filtered = df

    st.subheader("טבלת סיכום")
    st.dataframe(df_filtered, use_container_width=True)

    st.subheader("סיכום שעות לפי עובד")
    st.bar_chart(df_filtered.groupby("שם")["שעות עבודה"].sum())

    st.download_button("הורד דוח CSV", data=df_filtered.to_csv(index=False).encode('utf-8'), file_name="summary.csv")
