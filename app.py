import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Streamlit UI
st.title("📊 Event Log Analysis Dashboard")
st.write("Upload your Excel file to analyze event distributions.")

# File uploader
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file:
    # Load data
    data = pd.read_excel(uploaded_file)
    
    # Display dataset preview
    st.subheader("Data Preview")
    st.write(data.head())

    # Events grouped by device type
    events_by_device = data.groupby("Device_Type").size().reset_index(name="Count").sort_values(by="Count", ascending=False)

    # Plot event distribution by device type
    st.subheader("Event Distribution by Device Type")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x="Device_Type", y="Count", data=events_by_device, ax=ax, color="steelblue")
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Device Type")
    plt.ylabel("Number of Events")
    st.pyplot(fig)

    # Add failure, ESD, and local mode flags
    data["IsFailure"] = data["Event_Text"].str.contains("fail|failure", case=False, na=False).astype(int)
    data["ESD_Events"] = data["Event_Text"].str.contains("ESD", case=False, na=False).astype(int)
    data["Local_mode"] = data["Event_Text"].str.contains("Local", case=False, na=False).astype(int)

    # Failure events by device type
    failure_events_by_device = data.groupby("Device_Type")["IsFailure"].sum().reset_index().sort_values(by="IsFailure", ascending=False)

    # Plot failure events by device type
    st.subheader("Failure Events by Device Type")
    fig, ax = plt.subplots(figsize=(10,6))
    sns.barplot(x="Device_Type", y="IsFailure", data=failure_events_by_device, ax=ax, palette="coolwarm")
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Device Type")
    plt.ylabel("Number of Failure Events")
    st.pyplot(fig)

    st.success("Analysis Completed ✅")

