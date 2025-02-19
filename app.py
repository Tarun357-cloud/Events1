import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Event Analysis", layout="wide")

# Title
st.title("📊 Event Log Analysis Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    # Load data
    try:
        data = pd.read_excel(uploaded_file, header=0)
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]  # Remove unnamed columns
        data.columns = data.columns.str.strip().str.lower()  # Normalize column names (remove spaces, lowercase)
        st.subheader("Dataset Overview")
        st.write(data.head())  # Display first few rows

    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()  # Stop execution if file cannot be read

    # Ensure 'device_type' column exists
    if "device_type" not in data.columns:
        st.error("Error: 'Device_Type' column is missing from the uploaded file.")
        st.write("Columns found in the uploaded file:", list(data.columns))
        st.stop()  # Stop execution if the required column is missing

    # Events grouped by device type
    events_by_device = data.groupby("device_type").size().reset_index(name="Count").sort_values(by="Count", ascending=False)

    # Plot event distribution by device type
    st.subheader("Event Distribution by Device Type")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="device_type", y="Count", data=events_by_device, color="steelblue", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Device Type")
    plt.ylabel("Number of Events")
    st.pyplot(fig)

    # Ensure 'device_name' column exists
    if "device_name" in data.columns:
        # Events grouped by device type and name
        events_by_device_name = data.groupby(["device_type", "device_name"]).size().reset_index(name="Count")
        events_by_device_name = events_by_device_name.sort_values(by="Count", ascending=False).head(20)

        # Plot event distribution by device name and type
        st.subheader("Top 20 Devices with Most Events")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x="device_name", y="Count", hue="device_type", data=events_by_device_name, ax=ax)
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Device Name")
        plt.ylabel("Number of Events")
        st.pyplot(fig)

    # Ensure 'event_text' column exists
    if "event_text" in data.columns:
        # Add failure, ESD, and local mode flags
        data["isfailure"] = data["event_text"].str.contains("fail|failure", case=False, na=False).astype(int)
        data["esd_events"] = data["event_text"].str.contains("ESD", case=False, na=False).astype(int)
        data["local_mode"] = data["event_text"].str.contains("Local", case=False, na=False).astype(int)

        # Failure events by device type
        failure_events_by_device = data.groupby("device_type")["isfailure"].sum().reset_index().sort_values(by="isfailure", ascending=False)

        # Plot failure events by device type
        st.subheader("Failure Events by Device Type")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="device_type", y="isfailure", data=failure_events_by_device, palette="coolwarm", ax=ax)
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Device Type")
        plt.ylabel("Number of Failure Events")
        st.pyplot(fig)

    # Ensure 'device_name' exists for failure analysis
    if "device_name" in data.columns:
        # Failure events by device name
        failure_events_by_device_name = data.groupby("device_name")["isfailure"].sum().reset_index().sort_values(by="isfailure", ascending=False).head(20)

        # Plot failure events by device name
        st.subheader("Top 20 Devices with Most Failures")
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x="device_name", y="isfailure", data=failure_events_by_device_name, palette="coolwarm", ax=ax)
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Device Name")
        plt.ylabel("Number of Failure Events")
        st.pyplot(fig)

        # Failure rate calculation
        total_events_by_device_name = data.groupby("device_name").size().reset_index(name="Count")
        failure_events_by_device_name = failure_events_by_device_name.merge(total_events_by_device_name, on="device_name", how="left")
        failure_events_by_device_name["Failure_Rate (%)"] = (failure_events_by_device_name["isfailure"] / failure_events_by_device_name["Count"]) * 100
        failure_events_by_device_name = failure_events_by_device_name.sort_values(by="Failure_Rate (%)", ascending=False).head(20)

        # Plot failure rate by device type
        st.subheader("Failure Rate by Device Type")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x="device_name", y="Failure_Rate (%)", data=failure_events_by_device_name, palette="coolwarm", ax=ax)
        plt.xticks(rotation=45, ha="right")
        plt.xlabel("Device Name")
        plt.ylabel("Failure Rate (%)")
        st.pyplot(fig)

st.success("✅ Analysis Completed Successfully!")
