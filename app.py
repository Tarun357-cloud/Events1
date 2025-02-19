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
    data = pd.read_excel(uploaded_file)

    # Display dataframe info
    st.subheader("Dataset Overview")
    st.write(data.head())

    # Events grouped by device type
    events_by_device = data.groupby("Device_Type").size().reset_index(name="Count").sort_values(by="Count", ascending=False)

    # Plot event distribution by device type
    st.subheader("Event Distribution by Device Type")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Device_Type", y="Count", data=events_by_device, color="steelblue", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Device Type")
    plt.ylabel("Number of Events")
    st.pyplot(fig)

    # Events grouped by device type and name
    events_by_device_name = data.groupby(["Device_Type", "Device_Name"]).size().reset_index(name="Count")
    events_by_device_name = events_by_device_name.sort_values(by="Count", ascending=False).head(20)

    # Plot event distribution by device name and type
    st.subheader("Top 20 Devices with Most Events")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="Device_Name", y="Count", hue="Device_Type", data=events_by_device_name, ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Device Name")
    plt.ylabel("Number of Events")
    st.pyplot(fig)

    # Add failure, ESD, and local mode flags
    data["IsFailure"] = data["Event_Text"].str.contains("fail|failure", case=False, na=False).astype(int)
    data["ESD_Events"] = data["Event_Text"].str.contains("ESD", case=False, na=False).astype(int)
    data["Local_mode"] = data["Event_Text"].str.contains("Local", case=False, na=False).astype(int)

    # Failure events by device type
    failure_events_by_device = data.groupby("Device_Type")["IsFailure"].sum().reset_index().sort_values(by="IsFailure", ascending=False)

    # Failure events by device name
    failure_events_by_device_name = data.groupby("Device_Name")["IsFailure"].sum().reset_index().sort_values(by="IsFailure", ascending=False).head(20)

    # Local mode events by device name
    local_events_by_device_name = data.groupby("Device_Name")["Local_mode"].sum().reset_index().sort_values(by="Local_mode", ascending=False).head(20)

    # ESD events by device name
    esd_events_by_device_name = data.groupby("Device_Name")["ESD_Events"].sum().reset_index().sort_values(by="ESD_Events", ascending=False).head(20)

    # Plot failure events by device type
    st.subheader("Failure Events by Device Type")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Device_Type", y="IsFailure", data=failure_events_by_device, palette="coolwarm", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Device Type")
    plt.ylabel("Number of Failure Events")
    st.pyplot(fig)

    # Plot failure events by device name
    st.subheader("Top 20 Devices with Most Failures")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="Device_Name", y="IsFailure", data=failure_events_by_device_name, palette="coolwarm", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Device Name")
    plt.ylabel("Number of Failure Events")
    st.pyplot(fig)

    # Plot ESD events by device name
    st.subheader("Top 20 Devices with Most ESD Events")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="Device_Name", y="ESD_Events", data=esd_events_by_device_name, palette="viridis", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Device Name")
    plt.ylabel("Number of ESD Events")
    st.pyplot(fig)

    # Plot local events by device name
    st.subheader("Top 20 Devices with Most Local Mode Events")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="Device_Name", y="Local_mode", data=local_events_by_device_name, palette="magma", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Device Name")
    plt.ylabel("Number of Local Mode Events")
    st.pyplot(fig)

# Failure events by device type
    failure_events_by_device = data.groupby("Device_Type")["IsFailure"].sum().reset_index()
    failure_events_by_device = failure_events_by_device.merge(events_by_device, on="Device_Type", how="left")
    failure_events_by_device["Failure_Rate (%)"] = (failure_events_by_device["IsFailure"] / failure_events_by_device["Count"]) * 100

    # Failure events by device name
    failure_events_by_device_name = data.groupby("Device_Name")["IsFailure"].sum().reset_index()
    total_events_by_device_name = data.groupby("Device_Name").size().reset_index(name="Count")
    failure_events_by_device_name = failure_events_by_device_name.merge(total_events_by_device_name, on="Device_Name", how="left")
    failure_events_by_device_name["Failure_Rate (%)"] = (failure_events_by_device_name["IsFailure"] / failure_events_by_device_name["Count"]) * 100
    failure_events_by_device_name = failure_events_by_device_name.sort_values(by="Failure_Rate (%)", ascending=False).head(20)

    # Plot failure rate by device type
    st.subheader("Failure Rate by Device Type")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="Device_Type", y="Failure_Rate (%)", data=failure_events_by_device, palette="coolwarm", ax=ax)
    plt.xticks(rotation=45, ha="right")
    plt.xlabel("Device Type")
    plt.ylabel("Failure Rate (%)")
    st.pyplot(fig)
