import streamlit as st
import pandas as pd
from io import BytesIO
import openpyxl

def segregate_sheets(df, column_to_filter):
    unique_values = df[column_to_filter].unique()
    dataframes = {value: df[df[column_to_filter] == value] for value in unique_values}

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Write the original DataFrame to the main sheet
        df.to_excel(writer, sheet_name="Main Sheet", index=False)

        # Write each filtered DataFrame to a new sheet
        for value, data in dataframes.items():
            data.to_excel(writer, sheet_name=str(value), index=False)
        
    return output.getvalue()

st.title("Excel Sheet Segregator")

uploaded_file = st.file_uploader("Upload your Excel file", type=['xlsx'])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("Here is the preview of the uploaded file:")
        st.dataframe(df.head())

        columns = df.columns.tolist()
        column_to_filter = st.selectbox("Select the column to segregate by", columns)

        if st.button("Segregate and Download"):
            output_data = segregate_sheets(df, column_to_filter)
            st.success("Sheets created successfully!")

            st.download_button(
                label="Download segregated Excel file",
                data=output_data,
                file_name="segregated_data.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    except Exception as e:
        st.error(f"An error occurred: {e}")
