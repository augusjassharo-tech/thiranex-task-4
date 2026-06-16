import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Task 4: Data Cleaning", layout="wide")
st.title("Task 4: Data Cleaning & Reporting Automation")

uploaded_file = st.file_uploader("Choose CSV or Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("1. Raw Data Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Cells", df.isnull().sum().sum())
    st.dataframe(df.head(10))

    st.subheader("2. Data Quality Report")
    missing = df.isnull().sum()
    missing_df = missing[missing > 0].reset_index()
    missing_df.columns = ['Column', 'Missing Count']
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Missing Values:**")
        if len(missing_df) > 0:
            st.dataframe(missing_df)
        else:
            st.success("No missing values found")
    
    with col2:
        duplicates = df.duplicated().sum()
        st.metric("Duplicate Rows", duplicates)

    df_clean = df.copy().drop_duplicates().ffill().bfill()
    st.success(f"Cleaning Complete: Removed {duplicates} duplicates")

    st.subheader("3. Automated Visual Summary")
    # Use 'number' instead of np.number - no numpy import needed
    numeric_cols = df_clean.select_dtypes(include=['number']).columns.tolist()
    
    if len(numeric_cols) > 0:
        tab1, tab2 = st.tabs(["Summary Stats", "Distribution Plots"])
        with tab1:
            st.dataframe(df_clean[numeric_cols].describe())
        with tab2:
            selected_col = st.selectbox("Select column", numeric_cols)
            fig, ax = plt.subplots(figsize=(8, 4))
            df_clean[selected_col].hist(bins=20, ax=ax, color='skyblue', edgecolor='black')
            ax.set_title(f"Distribution of {selected_col}")
            st.pyplot(fig)
    else:
        st.warning("No numeric columns found")

    st.subheader("4. Download Cleaned Dataset")
    csv = df_clean.to_csv(index=False).encode('utf-8')
    st.download_button("Download cleaned_data.csv", csv, "cleaned_data.csv", "text/csv")

else:
    st.info("👆 Upload a CSV or Excel file to start")