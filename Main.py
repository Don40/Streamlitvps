import streamlit as st
import pandas as pd
from mysql_connection import *  
from numerize.numerize import numerize
import plotly.express as px

# Set page config
st.set_page_config(page_title="Analytics Dashboard", page_icon="🌎", layout="wide")  
st.subheader("📈 Business Analytics Dashboard")

# Load CSS Style
try:
    with open('style.css') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("CSS file not found. Default styles applied.")

# Initialize session state for data loading
if "data_loaded" not in st.session_state:
    st.session_state.data_loaded = False
    st.session_state.df = None  # Prevents errors before data is loaded

# Sidebar button to load data
if st.sidebar.button("Load Data"):
    st.session_state.df = pd.DataFrame(view_all_data(), columns=[
        "EEID", "FullName", "JobTitle", "Department", "BusinessUnit", "Gender", "Ethnicity", "Age", 
        "HireDate", "AnnualSalary", "Bonus", "Country", "City", "id"
    ])
    st.session_state.data_loaded = True  # Set flag to True

# Show message if data is not loaded
if not st.session_state.data_loaded:
    st.sidebar.info("Click 'Load Data' to display analytics.")
    st.stop()  # Stop execution until button is clicked

# Use the stored DataFrame
df = st.session_state.df  

# Sidebar filters (empty by default)
st.sidebar.header("Please filter")
department = st.sidebar.multiselect("Filter Department", options=df["Department"].unique(), default=[])
country = st.sidebar.multiselect("Filter Country", options=df["Country"].unique(), default=[])
businessunit = st.sidebar.multiselect("Filter Business", options=df["BusinessUnit"].unique(), default=[])

# Apply filters (show empty DataFrame if no filters selected)
if department or country or businessunit:
    df_selection = df.query("Department == @department & Country == @country & BusinessUnit == @businessunit")
else:
    df_selection = df.iloc[0:0]  # Empty DataFrame

# Define analytics functions
def metrics():
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Customers", value=df_selection.Gender.count(), delta="All customers")
    col2.metric(label="Total Annual Salary", value=f"{df_selection.AnnualSalary.sum():,.0f}", delta=f"{df.AnnualSalary.median():,.0f}")
    col3.metric(label="Annual Salary Range", value=f"{df_selection.AnnualSalary.max()-df.AnnualSalary.min():,.0f}", delta="")
    style_metric_cards(background_color="#071021", border_left_color="#1f66bd")

div1, div2 = st.columns(2)

def pie():
    if not df_selection.empty:
        with div1:
            fig = px.pie(df_selection, values='AnnualSalary', names='Department', title='Customers by Department')
            fig.update_layout(legend_title="Department", legend_y=0.9)
            fig.update_traces(textinfo='percent+label', textposition='inside')
            st.plotly_chart(fig, use_container_width=True)

def barchart():
    if not df_selection.empty:
        with div2:
            fig = px.bar(df_selection, y='AnnualSalary', x='Department', text_auto='.2s', title="Annual Salary by Department")
            fig.update_traces(textfont_size=14, textangle=0, textposition="outside", cliponaxis=False)
            st.plotly_chart(fig, use_container_width=True)

def table():
    if not df_selection.empty:
        with st.expander("Tabular Data"):
            shwdata = st.multiselect('Filter Columns:', df.columns, 
                                    default=["EEID", "FullName", "JobTitle", "Department", 
                                             "BusinessUnit", "Gender", "Ethnicity", "Age", 
                                             "HireDate", "AnnualSalary", "Bonus", "Country", "City"])
            st.dataframe(df_selection[shwdata], use_container_width=True)
            st.write(df_selection.describe().T)

# Sidebar option menu
from streamlit_option_menu import option_menu
with st.sidebar:
    selected = option_menu(
        menu_title="Main Menu",
        options=["Home", "Table"],
        icons=["house", "table"],
        menu_icon="cast",
        default_index=0
    )

# Render selected page
if selected == "Home":
    pie()
    barchart()
    metrics()
elif selected == "Table":
    metrics()
    table()
