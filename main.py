import streamlit as st
import pandas as pd
from io import BytesIO


st.set_page_config(page_title="File Converter & Cleaner", layout="wide")

st.title("📂File Converter & Cleaner")
st.write("Upload your CSV and Excel Files to clean data and convert formats effortlessly")
files = st.file_uploader("Upload csv or Excel files.", type=["csv", "xlsx"], accept_multiple_files=True)

if files:  # Check if there are any files uploaded
    for file in files:  # Loop through the uploaded files
        ext = file.name.split(".")[-1]  # Get file extension

        # Check if file is CSV or Excel, and read accordingly
        if ext == "csv":
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")  # Correctly referencing file name
        st.dataframe(df.head())  # Display first few rows of the file's data

        if st.checkbox(f"Fill missing values - {file.name}"):
            # Fill missing values with the mean of numerical columns
            df.fillna(df.select_dtypes(include="number").mean(), inplace=True)
            st.success(f"Missing values filled successfully in {file.name}!")
            st.dataframe(df.head())  # Display updated data

        # Select columns
        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]  # Only keep selected columns
        st.dataframe(df.head())

        if st.checkbox(f"📊 Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"⬇ Download {file.name} as {format_choice}"):
            # Initialize BytesIO stream
            output = BytesIO()  # Correctly initialized here
            new_name = file.name  # Initialize the name

            if format_choice == "CSV":
                df.to_csv(output, index=False)
                output.seek(0)  # Set the pointer back to the start of the BytesIO stream
                mime = "text/csv"
                new_name = file.name.replace(ext, "csv")  # Replace extension with 'csv'
            else:
                df.to_excel(output, index=False)
                output.seek(0)  # Set the pointer back to the start of the BytesIO stream
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                new_name = file.name.replace(ext, "xlsx")  # Replace extension with 'xlsx'

            # Now use the stream with st.download_button
            st.download_button(label= f"⬇ Download {file.name} as {format_choice}", 
                               data=output, file_name=new_name, mime=mime)
            st.success("Processing Completed!")
#new_env\Scripts\activate
# pip install streamlit
# streamlit run Password.py new_env\Scripts\activate
# pip install streamlit
# streamlit run Password.py
# pip install streamlit
# streamlit run Password.py