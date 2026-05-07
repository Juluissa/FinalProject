import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Hospital Readmission Dashboard")



df = pd.read_csv("FY_2026_Hospital_Readmissions_Reduction_Program_Hospital.csv")

df["Excess Readmission Ratio"] = pd.to_numeric(df["Excess Readmission Ratio"], errors="coerce")
df["Number of Discharges"] = pd.to_numeric(df["Number of Discharges"], errors="coerce")
df["Expected Readmission Rate"] = pd.to_numeric(df["Expected Readmission Rate"], errors="coerce")
df["Predicted Readmission Rate"] = pd.to_numeric(df["Predicted Readmission Rate"], errors="coerce")


df = df.dropna()
df = df.drop_duplicates()

Q1 = df["Excess Readmission Ratio"].quantile(0.25)
Q3 = df["Excess Readmission Ratio"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

clean_df = df[
    (df["Excess Readmission Ratio"] >= lower) &
    (df["Excess Readmission Ratio"] <= upper)
].copy()


st.subheader("Dashboard Summary")

col1, col2, col3 = st.columns(3)

col1.metric("Rows Shown", len(clean_df))
col2.metric(
    "Average Readmission Ratio",
    round(clean_df["Excess Readmission Ratio"].mean(), 3)
)
col3.metric(
    "Average Discharges",
    round(clean_df["Number of Discharges"].mean(), 1)
)

# Graph 1: Top 10 States by Count
st.subheader("Top 10 States by Count")

state_counts = (
    clean_df["State"]
    .value_counts()
    .head(10)
    .reset_index()
)

state_counts.columns = ["State", "Count"]

fig1 = px.bar(
    state_counts,
    x="State",
    y="Count",
    color="Count",
    color_continuous_scale="Blues",
    title="Top 10 States by Count"
)

fig1.update_layout(
    xaxis_title="State",
    yaxis_title="Count"
)

st.plotly_chart(fig1, use_container_width=True)

st.write("This graph shows the 10 states with the most hospital records.")

# Graph 2: Expected vs Predicted
st.subheader("Expected vs Predicted Readmission Rate")

fig2 = px.scatter(
    clean_df,
    x="Expected Readmission Rate",
    y="Predicted Readmission Rate",
    title="Expected vs Predicted Readmission Rate",
    hover_data=["Facility Name", "State", "Measure Name"]
)

fig2.update_layout(
    xaxis_title="Expected Readmission Rate",
    yaxis_title="Predicted Readmission Rate"
)

st.plotly_chart(fig2, use_container_width=True)

st.write("This graph compares expected readmission rates to predicted readmission rates.")

# Graph 3: Measure Count
st.subheader("Measure Count")

measure_counts = (
    clean_df["Measure Name"]
    .value_counts()
    .reset_index()
)

measure_counts.columns = ["Measure Name", "Count"]

fig3 = px.bar(
    measure_counts,
    x="Measure Name",
    y="Count",
    title="Count of Each Measure Type",
    color = "Measure Name",
    color_continuous_scale = ""

)

fig3.update_layout(
    xaxis_title="Measure Name",
    yaxis_title="Count",
    xaxis_tickangle=45
)

st.plotly_chart(fig3, use_container_width=True)

st.write("This graph shows how often each readmission measure appears in the dataset.")

# Graph 4: Discharges vs Readmission Ratio
st.subheader("Discharges vs Readmission Ratio")

fig4 = px.scatter(
    clean_df,
    x="Number of Discharges",
    y="Excess Readmission Ratio",
    color="State",
    hover_data=["Facility Name", "Measure Name"],
    title="Discharges vs Readmission Ratio"
)

fig4.update_layout(
    xaxis_title="Number of Discharges",
    yaxis_title="Excess Readmission Ratio"
)

st.plotly_chart(fig4, use_container_width=True)

st.write("This graph checks if hospitals with more discharges have higher readmission ratios.")

# Data Preview
st.subheader("Data Preview")

st.dataframe(clean_df.head(20))