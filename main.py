import streamlit as st
import pandas as pd
import seaborn as sns

uploaded_file = st.file_uploader("Time-Wasters on Social Media.csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
else:
    st.warning("Time-Wasters on Social Media.csv")

@st.cache  # Cache the data to improve performance
def load_data():
    return pd.read_csv('Time-Wasters on Social Media.csv')  # Update with the correct path

data = load_data()

data.head()

st.title("Time-Wasters on Social Media Analysis")
st.write("""
    This app provides insights into social media usage patterns and the impact on user productivity.
    Use the filters and interactive elements to explore the data.
""")

st.sidebar.header("Filter Data")

# Age filter
age_filter = st.sidebar.slider("Select Age Range", int(data.Age.min()), int(data.Age.max()), (20, 50))

# Gender filter
gender_filter = st.sidebar.multiselect("Select Gender", options=data.Gender.unique(), default=data.Gender.unique())

# Platform filter
platform_filter = st.sidebar.multiselect("Select Platform", options=data.Platform.unique(), default=data.Platform.unique())

# Filter the data based on the selected options
filtered_data = data[(data['Age'] >= age_filter[0]) & (data['Age'] <= age_filter[1]) &
                     (data['Gender'].isin(gender_filter)) &
                     (data['Platform'].isin(platform_filter))]


st.subheader("Key Performance Indicators")
st.metric("Total Time Spent (hours)", int(filtered_data['Total Time Spent'].sum()))
st.metric("Average Productivity Loss", round(filtered_data['ProductivityLoss'].mean(), 2))
st.metric("Average Addiction Level", round(filtered_data['Addiction Level'].mean(), 2))

st.subheader("Age Distribution of Users")
fig, ax = plt.subplots()
st.histplot(filtered_data['Age'], bins=20, ax=ax)
st.pyplot(fig)


st.subheader("Platform Usage by Total Time Spent")
platform_time = filtered_data.groupby('Platform')['Total Time Spent'].sum().sort_values()
st.bar_chart(platform_time)

st.subheader("User Engagement by Video Category")

fig, ax = plt.subplots()
st.boxplot(data=filtered_data, x='Video Category', y='Engagement', ax=ax)
st.pyplot(fig)


st.subheader("Scroll Rate vs. Productivity Loss")
fig, ax = plt.subplots()
st.scatter_plot(data=filtered_data, x='Scroll Rate', y='ProductivityLoss', hue='Platform', ax=ax)
st.pyplot(fig)

# Slider for selecting Addiction Level range
addiction_slider = st.slider("Select Addiction Level Range", int(data['Addiction Level'].min()), int(data['Addiction Level'].max()), (1, 10))
filtered_data = filtered_data[(filtered_data['Addiction Level'] >= addiction_slider[0]) & (filtered_data['Addiction Level'] <= addiction_slider[1])]

# Checkbox for displaying raw data
if st.checkbox("Show Raw Data"):
    st.write(filtered_data)

