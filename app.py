import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(
    page_title="🚀 Futuristic Silver BI Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h1 class='main-header'>Futuristic Silver BI Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-powered business insights and management</p>", unsafe_allow_html=True)

# ------------------------
# CSV FILES
# ------------------------
csv_files = {
    "Sales Tracking": "sales_tracking.csv",
    "Products": "products.csv",
    "Follow-Ups": "follow_ups.csv",
    "Invoices": "invoices.csv",
    "Subscriptions": "subscriptions.csv",
    "Support & Tickets": "support_tickets.csv",
    "Project Management": "project_management.csv",
    "Team Management": "team_management.csv"
}

# ------------------------
# LOAD CSV WITH CACHE
# ------------------------
@st.cache_data
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        df.columns = [c.strip() for c in df.columns]
        # Convert dates
        for col in df.columns:
            if any(x in col.lower() for x in ['date', 'start', 'end', 'created', 'due']):
                df[col] = pd.to_datetime(df[col], errors='coerce')
        return df
    except:
        return pd.DataFrame()

# ------------------------
# SIDEBAR NAVIGATION
# ------------------------
selected_csv = st.sidebar.selectbox("Select CSV / Module", list(csv_files.keys()))
df = load_csv(csv_files[selected_csv])
st.subheader(f"{selected_csv} ({df.shape[0]} rows)")

# ------------------------
# FILTERS
# ------------------------
def render_filters(df):
    filters = {}
    for col in df.select_dtypes(include=['object', 'category']).columns:
        unique_vals = df[col].dropna().unique()
        if len(unique_vals) > 1 and len(unique_vals) <= 50:
            selected = st.sidebar.multiselect(f"Filter {col}", unique_vals, default=unique_vals)
            filters[col] = selected
    filtered_df = df.copy()
    for col, vals in filters.items():
        filtered_df = filtered_df[filtered_df[col].isin(vals)]
    return filtered_df

df_filtered = render_filters(df)

# ------------------------
# SUMMARY METRICS
# ------------------------
def render_metrics(df, module_name):
    if module_name == "Sales Tracking":
        total_deals = len(df)
        won_deals = len(df[df['Status'] == 'Closed Won']) if 'Status' in df.columns else 0
        revenue = df['Deal Value'].sum() if 'Deal Value' in df.columns else 0
        st.metric("Total Deals", total_deals)
        st.metric("Closed Won Deals", won_deals)
        st.metric("Total Revenue", f"${revenue:,.0f}")
    elif module_name == "Products":
        total_products = len(df)
        active_users = df['Active Users'].sum() if 'Active Users' in df.columns else 0
        mrr = df['Monthly Recurring Revenue'].sum() if 'Monthly Recurring Revenue' in df.columns else 0
        st.metric("Total Products", total_products)
        st.metric("Active Users", active_users)
        st.metric("Monthly Revenue", f"${mrr:,.0f}")
    elif module_name == "Support & Tickets":
        total_tickets = len(df)
        open_tickets = len(df[df['Status'].isin(['Open','In Progress'])]) if 'Status' in df.columns else 0
        avg_satisfaction = df['Customer Satisfaction'].mean() if 'Customer Satisfaction' in df.columns else 0
        st.metric("Total Tickets", total_tickets)
        st.metric("Open Tickets", open_tickets)
        st.metric("Avg Customer Satisfaction", f"{avg_satisfaction:.1f}/5")
    elif module_name == "Project Management":
        total_projects = len(df)
        in_progress = len(df[df['Status'] == 'In Progress']) if 'Status' in df.columns else 0
        total_budget = df['Budget'].sum() if 'Budget' in df.columns else 0
        st.metric("Total Projects", total_projects)
        st.metric("In Progress", in_progress)
        st.metric("Total Budget", f"${total_budget:,.0f}")
    elif module_name == "Team Management":
        total_team = len(df)
        avg_salary = df['Salary'].mean() if 'Salary' in df.columns else 0
        avg_perf = df['Performance Score'].mean() if 'Performance Score' in df.columns else 0
        st.metric("Total Employees", total_team)
        st.metric("Average Salary", f"${avg_salary:,.0f}")
        st.metric("Average Performance", f"{avg_perf:.1f}/5")
    elif module_name == "Invoices":
        total_invoices = len(df)
        total_paid = len(df[df['Status']=='Paid']) if 'Status' in df.columns else 0
        total_amount = df['Price'].sum() if 'Price' in df.columns else 0
        st.metric("Total Invoices", total_invoices)
        st.metric("Paid", total_paid)
        st.metric("Total Amount", f"${total_amount:,.0f}")
    elif module_name == "Subscriptions":
        total_subs = len(df)
        active_subs = len(df[df['Status']=='Active']) if 'Status' in df.columns else 0
        total_revenue = df['Price'].sum() if 'Price' in df.columns else 0
        st.metric("Total Subscriptions", total_subs)
        st.metric("Active", active_subs)
        st.metric("Total Revenue", f"${total_revenue:,.0f}")
    elif module_name == "Follow-Ups":
        total_followups = len(df)
        upcoming = len(df[df['Next Follow-Up Date'] >= pd.Timestamp.today()]) if 'Next Follow-Up Date' in df.columns else 0
        st.metric("Total Follow-Ups", total_followups)
        st.metric("Upcoming Follow-Ups", upcoming)

render_metrics(df_filtered, selected_csv)

# ------------------------
# CHARTS
# ------------------------
def render_charts(df, module_name):
    if module_name == "Sales Tracking" and 'Deal Value' in df.columns:
        fig = px.bar(df, x='Sales Rep', y='Deal Value', color='Status', title='Deal Value by Sales Rep')
        st.plotly_chart(fig, use_container_width=True)
    if module_name == "Products" and 'Monthly Recurring Revenue' in df.columns:
        fig = px.pie(df, names='Product Name', values='Monthly Recurring Revenue', title='MRR by Product')
        st.plotly_chart(fig, use_container_width=True)
    if module_name == "Support & Tickets":
        fig = px.histogram(df, x='Priority', color='Status', barmode='group', title='Tickets by Priority & Status')
        st.plotly_chart(fig, use_container_width=True)
    if module_name == "Project Management":
        fig = px.bar(df, x='Project Name', y='Budget', color='Status', title='Project Budgets by Status')
        st.plotly_chart(fig, use_container_width=True)
    if module_name == "Team Management":
        fig = px.bar(df, x='Full Name', y='Salary', color='Department', title='Team Salaries by Department')
        st.plotly_chart(fig, use_container_width=True)
    if module_name == "Invoices":
        fig = px.bar(df, x='Customer', y='Price', color='Status', title='Invoices by Customer & Status')
        st.plotly_chart(fig, use_container_width=True)
    if module_name == "Subscriptions":
        fig = px.pie(df, names='Product', values='Price', title='Revenue by Subscription')
        st.plotly_chart(fig, use_container_width=True)
    if module_name == "Follow-Ups" and 'Next Follow-Up Date' in df.columns:
        df['Next Follow-Up Date'] = pd.to_datetime(df['Next Follow-Up Date'], errors='coerce')
        fig = px.timeline(df, x_start=pd.Timestamp.today(), x_end='Next Follow-Up Date', y='Client Name', color='Status', title='Upcoming Follow-Ups Timeline')
        st.plotly_chart(fig, use_container_width=True)

render_charts(df_filtered, selected_csv)

# ------------------------
# CARD DISPLAY FUNCTION
# ------------------------
def render_cards(dataframe, max_cols=3):
    for idx in range(0, len(dataframe), max_cols):
        cols = st.columns(max_cols)
        for col, (_, row) in zip(cols, dataframe.iloc[idx:idx+max_cols].iterrows()):
            with col:
                st.markdown("<div class='data-card'>", unsafe_allow_html=True)
                # Card title
                title_col = next((c for c in ['Client Name', 'Project Name', 'Full Name', 'Product Name'] if c in dataframe.columns), None)
                if title_col:
                    st.markdown(f"<div class='card-title'>{row[title_col]}</div>", unsafe_allow_html=True)
                for c in dataframe.columns:
                    value = row[c]
                    if pd.isnull(value):
                        value = "-"
                    st.markdown(f"<div class='card-field'><span class='field-label'>{c}:</span> <span class='field-value'>{value}</span></div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

render_cards(df_filtered)
