import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set Streamlit page config
st.set_page_config(page_title="Event Analysis", layout="wide")

st.title("📊 Event Log Analysis Dashboard")

uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

if uploaded_file:
    try:
        data = pd.read_excel(uploaded_file, header=0)
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        data.columns = data.columns.str.strip().str.lower()
        st.subheader("Dataset Overview")
        st.write(data.head())
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    required_columns = ["device_type", "device_name", "event_text"]
    for col in required_columns:
        if col not in data.columns:
            st.error(f"Error: '{col}' column is missing from the uploaded file.")
            st.write("Columns found in the uploaded file:", list(data.columns))
            st.stop()

    events_by_device = data.groupby("device_type").size().reset_index(name="Count").sort_values(by="Count", ascending=False)
    st.subheader("Event Distribution by Device Type")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="device_type", y="Count", data=events_by_device, color="steelblue", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    events_by_device_name = data.groupby(["device_type", "device_name"]).size().reset_index(name="Count")
    events_by_device_name = events_by_device_name.sort_values(by="Count", ascending=False).head(20)
    st.subheader("Top 20 Devices with Most Events")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="device_name", y="Count", hue="device_type", data=events_by_device_name, ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    data["isfailure"] = data["event_text"].str.contains("fail|failure", case=False, na=False).astype(int)
    data["esd_events"] = data["event_text"].str.contains("ESD", case=False, na=False).astype(int)
    data["local_mode"] = data["event_text"].str.contains("Local", case=False, na=False).astype(int)

    failure_events_by_device = data.groupby("device_type")["isfailure"].sum().reset_index().sort_values(by="isfailure", ascending=False)
    st.subheader("Failure Events by Device Type")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="device_type", y="isfailure", data=failure_events_by_device, palette="coolwarm", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    failure_events_by_device_name = data.groupby("device_name")["isfailure"].sum().reset_index().sort_values(by="isfailure", ascending=False).head(20)
    st.subheader("Top 20 Devices with Most Failures")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="device_name", y="isfailure", data=failure_events_by_device_name, palette="coolwarm", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    esd_events_by_device_name = data.groupby("device_name")["esd_events"].sum().reset_index().sort_values(by="esd_events", ascending=False).head(20)
    st.subheader("Top 20 Devices with Most ESD Events")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="device_name", y="esd_events", data=esd_events_by_device_name, palette="viridis", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    local_events_by_device_name = data.groupby("device_name")["local_mode"].sum().reset_index().sort_values(by="local_mode", ascending=False).head(20)
    st.subheader("Top 20 Devices with Most Local Mode Events")
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="device_name", y="local_mode", data=local_events_by_device_name, palette="magma", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

    failure_events_by_device = failure_events_by_device.merge(events_by_device, on="device_type", how="left")
    failure_events_by_device["Failure_Rate (%)"] = (failure_events_by_device["isfailure"] / failure_events_by_device["Count"]) * 100
    st.subheader("Failure Rate by Device Type")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x="device_type", y="Failure_Rate (%)", data=failure_events_by_device, palette="coolwarm", ax=ax)
    plt.xticks(rotation=45, ha="right")
    st.pyplot(fig)

st.success("✅ Analysis Completed Successfully!")
