"""
Economic Model

This is the main file for the Economic Model Streamlit application.
It reads data from xlsx and displays it in an interactive dashboard.
"""

import streamlit as st
from loaders.excel_loader import ExcelDataLoader
from plots.plots import (
    create_unlock_plot,
    create_unlock_pie_chart,
    create_unlock_column_chart,
    create_unlock_emission_plot,
    create_absolute_issuance_plot,
    create_relative_issuance_plot,
    create_issuance_ratio_plot,
)
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go

# Add this near the top of your file, after the imports
st.set_page_config(
    page_title="Economic Model",
    layout="wide",
    initial_sidebar_state="collapsed",
    # Add theme configuration
    menu_items={"Get Help": None, "Report a bug": None, "About": None},
)


def display_latest_cumulative_data(df: pd.DataFrame, selected_month=None):
    """Display cumulative data for selected month in a styled window format.

    Args:
        df: DataFrame containing cumulative data
        selected_month: Selected month to display data for, if None shows latest
    """
    # Get the data for selected month or latest if none selected
    if selected_month is not None:
        data = df[df["Month"] == selected_month].iloc[0]
    else:
        data = df.iloc[-1]

    # Get cumulative columns
    cumulative_cols = [col for col in df.columns if "Cumulative " in str(col)]

    # Create two columns for layout
    cols = st.columns(2)

    # Display each value with label in alternating columns
    for i, col in enumerate(cumulative_cols):
        col_index = i % 2
        with cols[col_index]:
            # Clean up label by removing 'Cumulative ' prefix
            label = col.replace("Cumulative ", "")
            if "Circulating Supply %" in col:
                value = f"{data[col]}"  # Keep string format for percentage
            else:
                value = f"{data[col]:,.0f}"  # Format numbers with commas

            # Create a container with custom styling
            if "Emission" in label:
                st.markdown(
                    f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #ffffff;
                        margin: 8px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #e0e0e0;
                        width: 100%;  /* Full width */
                '>
                    <p style='
                        color: #666666;
                        font-size: 0.9em;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 8px;
                    '>{label}</p>
                    <p style='
                        color: #1f2937;
                        font-size: 1.6em;
                        font-weight: 600;
                        margin: 0;
                    '>{value}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #ffffff;
                        margin: 8px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #e0e0e0;
                    '>
                    <p style='
                        color: #666666;
                        font-size: 0.9em;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 8px;
                    '>{label}</p>
                    <p style='
                        color: #1f2937;
                        font-size: 1.6em;
                        font-weight: 600;
                        margin: 0;
                    '>{value}</p>
                </div>
                """,
                    unsafe_allow_html=True,
                )


def display_monthly_data(df: pd.DataFrame, selected_month=None):
    """Display monthly (non-cumulative) data in a styled window format."""
    # Get the data for selected month or latest if none selected
    if selected_month is not None:
        data = df[df["Month"] == selected_month].iloc[0]
    else:
        data = df.iloc[-1]

    # Get non-cumulative columns
    monthly_cols = [
        col
        for col in df.columns
        if "Cumulative " not in str(col)
        and "Month" not in str(col)
        and "Date" not in str(col)
    ]

    # Create two columns for layout
    cols = st.columns(2)

    # Display each value with label in alternating columns
    # Group columns into Unlock and Other categories
    unlock_cols = [
        "Investors+Seed",
        "Investors+Series",
        "Team",
        "Airdrop",
        "Future Initiatives",
        "R&D and Ecosystem",
        "Total Unlock",
    ]
    other_cols = [col for col in monthly_cols if col not in unlock_cols]

    # Display Unlock header
    st.subheader("Unlock")
    cols_unlock = st.columns(2)
    for i, col in enumerate(unlock_cols):
        if col in monthly_cols:
            col_index = i % 2
            with cols_unlock[col_index]:
                # Format value based on whether it's a percentage or number
                if "Circulating Supply %" in col:
                    value = f"{data[col]*100:,.0f}%"
                elif col == "Total Unlock":
                    continue
                else:
                    value = f"{data[col]:,.0f}"

                st.markdown(
                    f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #ffffff;
                        margin: 8px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #e0e0e0;
                    '>
                        <p style='
                            color: #666666;
                            font-size: 0.9em;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            margin-bottom: 8px;
                        '>{col}</p>
                        <p style='
                            color: #1f2937;
                            font-size: 1.6em;
                            font-weight: 600;
                            margin: 0;
                        '>{value}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
    # Then display Total Unlock in full width
    if "Total Unlock" is col:
        value = f"{data['Total Unlock']:,.0f}"
        st.markdown(
            f"""
            <div style='
                padding: 15px;
                border-radius: 10px;
                background-color: #ffffff;
                margin: 8px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0;
                width: 100%;  /* Full width */
            '>
                <p style='
                    color: #666666;
                    font-size: 0.9em;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 8px;
                '>Total Unlock</p>
                <div style='
                    display: flex;
                    align-items: center;
                    justify-content: center;
                '>
                    <p style='
                        color: #1f2937;
                        font-size: 1.6em;
                        font-weight: 600;
                        margin: 0;
                    '>{value}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Display Cumulative Total header
    if other_cols:
        st.subheader("Cumulative Total")
        cols_other = st.columns(2)
        for i, col in enumerate(other_cols):
            col_index = i % 2
            with cols_other[col_index]:
                # Format value based on whether it's a percentage or number
                if "Circulating Supply %" in col:
                    value = f"{data[col]*100:,.0f}%"
                else:
                    value = f"{data[col]:,.0f}"

                st.markdown(
                    f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #ffffff;
                        margin: 8px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #e0e0e0;
                        height: 300px;
                    '>
                        <p style='
                            color: #666666;
                            font-size: 0.9em;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            margin-bottom: 8px;
                        '>{col}</p>
                        <div style='
                            height: calc(100% - 40px);
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        '>
                            <p style='
                                color: #1f2937;
                                font-size: 1.6em;
                                font-weight: 600;
                                margin: 0;
                            '>{value}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def display_yearly_data(df: pd.DataFrame, selected_year=None):
    """Display yearly aggregated data in a styled window format."""
    # Get the data for selected year or latest if none selected

    selected_year = selected_year * 12
    if selected_year is not None:
        # Find the index of selected month
        month_index = df[df["Month"] == selected_year].index[0]
        # Calculate start index for 12 months before
        start_index = max(0, month_index - 11)
        # Get the data for the year
        year_data = df.iloc[start_index : month_index + 1]
    else:
        # Get last 12 months
        year_data = df.iloc[-12:]

    # Get non-cumulative columns
    monthly_cols = [
        col
        for col in df.columns
        if "Cumulative " not in str(col)
        and "Month" not in str(col)
        and "Date" not in str(col)
    ]

    # Create aggregated data
    data = pd.Series()

    # Sum up regular columns
    for col in monthly_cols:
        if "Circulating Supply %" not in col:
            data[col] = year_data[col].sum()

    # For Circulating Supply %, take the last month's value
    circulating_cols = [
        col
        for col in df.columns
        if "Circulating Supply %" in col
        or "Cumulative" in col
        and "Cumulative " not in col
    ]
    for col in circulating_cols:
        data[col] = year_data.iloc[-1][col]

    # Group columns into Unlock and Other categories
    unlock_cols = [
        "Investors+Seed",
        "Investors+Series",
        "Team",
        "Airdrop",
        "Future Initiatives",
        "R&D and Ecosystem",
        "Total Unlock",
    ]
    other_cols = [col for col in monthly_cols if col not in unlock_cols]

    # Add Circulating Supply % to other_cols if not already present
    other_cols.extend([col for col in circulating_cols if col not in other_cols])

    # Display Unlock header
    st.subheader("Yearly Unlock")
    cols_unlock = st.columns(2)
    for i, col in enumerate(unlock_cols):
        if col in monthly_cols:
            col_index = i % 2
            with cols_unlock[col_index]:
                # Format value based on whether it's a percentage or number
                if "Circulating Supply %" in col:
                    value = f"{data[col]*100:,.0f}%"
                elif col == "Total Unlock":
                    continue
                else:
                    value = f"{data[col]:,.0f}"

                st.markdown(
                    f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #ffffff;
                        margin: 8px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #e0e0e0;
                    '>
                        <p style='
                            color: #666666;
                            font-size: 0.9em;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            margin-bottom: 8px;
                        '>{col}</p>
                        <p style='
                            color: #1f2937;
                            font-size: 1.6em;
                            font-weight: 600;
                            margin: 0;
                        '>{value}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Display Total Unlock in full width
    if "Total Unlock" in monthly_cols:
        value = f"{data['Total Unlock']:,.0f}"
        st.markdown(
            f"""
            <div style='
                padding: 15px;
                border-radius: 10px;
                background-color: #ffffff;
                margin: 8px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0;
                width: 100%;
            '>
                <p style='
                    color: #666666;
                    font-size: 0.9em;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 8px;
                '>Total Yearly Unlock</p>
                <div style='
                    display: flex;
                    align-items: center;
                    justify-content: center;
                '>
                    <p style='
                        color: #1f2937;
                        font-size: 1.6em;
                        font-weight: 600;
                        margin: 0;
                    '>{value}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    # Display Cumulative Total header
    if other_cols:
        st.subheader("Cumulative Total")
        cols_other = st.columns(2)
        for i, col in enumerate(other_cols):
            col_index = i % 2
            with cols_other[col_index]:
                # Format value based on whether it's a percentage or number
                if "Circulating Supply %" in col:
                    value = f"{data[col]*100:,.0f}%"
                else:
                    value = f"{data[col]:,.0f}"

                st.markdown(
                    f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #ffffff;
                        margin: 8px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #e0e0e0;
                        height: 300px;
                    '>
                        <p style='
                            color: #666666;
                            font-size: 0.9em;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            margin-bottom: 8px;
                        '>{col}</p>
                        <div style='
                            height: calc(100% - 40px);
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        '>
                            <p style='
                                color: #1f2937;
                                font-size: 1.6em;
                                font-weight: 600;
                                margin: 0;
                            '>{value}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def display_quarterly_data(df: pd.DataFrame, selected_quarter=None):
    """Display quarterly aggregated data in a styled window format."""
    # Get the data for selected quarter or latest if none selected
    if selected_quarter is not None:
        # Convert quarter to month (each quarter is 3 months)
        selected_month = selected_quarter * 3

        # Find the index of selected month
        month_index = df[df["Month"] == selected_month].index[0]
        # Calculate start index for 3 months before
        start_index = max(0, month_index - 2)  # 3 months total
        # Get the data for the quarter
        quarter_data = df.iloc[start_index : month_index + 1]
    else:
        # Get last 3 months
        quarter_data = df.iloc[-3:]

    # Get non-cumulative columns
    monthly_cols = [
        col
        for col in df.columns
        if "Cumulative " not in str(col)
        and "Month" not in str(col)
        and "Date" not in str(col)
    ]

    # Create aggregated data
    data = pd.Series()

    # Sum up regular columns
    for col in monthly_cols:
        if "Circulating Supply %" not in col:
            data[col] = quarter_data[col].sum()

    # For Circulating Supply %, take the last month's value
    circulating_cols = [
        col
        for col in df.columns
        if "Circulating Supply %" in col
        or "Cumulative" in col
        and "Cumulative " not in col
    ]
    for col in circulating_cols:
        data[col] = quarter_data.iloc[-1][col]

    # Group columns into Unlock and Other categories
    unlock_cols = [
        "Investors+Seed",
        "Investors+Series",
        "Team",
        "Airdrop",
        "Future Initiatives",
        "R&D and Ecosystem",
        "Total Unlock",
    ]
    other_cols = [col for col in monthly_cols if col not in unlock_cols]

    # Add Circulating Supply % to other_cols if not already present
    other_cols.extend([col for col in circulating_cols if col not in other_cols])

    # Display Unlock header
    st.subheader("Quarterly Unlock")
    cols_unlock = st.columns(2)
    for i, col in enumerate(unlock_cols):
        if col in monthly_cols:
            col_index = i % 2
            with cols_unlock[col_index]:
                # Format value based on whether it's a percentage or number
                if "Circulating Supply %" in col:
                    value = f"{data[col]*100:,.0f}%"
                elif col == "Total Unlock":
                    continue
                else:
                    value = f"{data[col]:,.0f}"

                st.markdown(
                    f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #ffffff;
                        margin: 8px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #e0e0e0;
                    '>
                        <p style='
                            color: #666666;
                            font-size: 0.9em;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            margin-bottom: 8px;
                        '>{col}</p>
                        <p style='
                            color: #1f2937;
                            font-size: 1.6em;
                            font-weight: 600;
                            margin: 0;
                        '>{value}</p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Display Total Unlock in full width
    if "Total Unlock" in monthly_cols:
        value = f"{data['Total Unlock']:,.0f}"
        st.markdown(
            f"""
            <div style='
                padding: 15px;
                border-radius: 10px;
                background-color: #ffffff;
                margin: 8px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border: 1px solid #e0e0e0;
                width: 100%;
            '>
                <p style='
                    color: #666666;
                    font-size: 0.9em;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                    margin-bottom: 8px;
                '>Total Quarterly Unlock</p>
                <div style='
                    display: flex;
                    align-items: center;
                    justify-content: center;
                '>
                    <p style='
                        color: #1f2937;
                        font-size: 1.6em;
                        font-weight: 600;
                        margin: 0;
                    '>{value}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Display Cumulative Total header
    if other_cols:
        st.subheader("Cumulative Total")
        cols_other = st.columns(2)
        for i, col in enumerate(other_cols):
            col_index = i % 2
            with cols_other[col_index]:
                # Format value based on whether it's a percentage or number
                if "Circulating Supply %" in col:
                    value = f"{data[col]*100:,.0f}%"
                else:
                    value = f"{data[col]:,.0f}"

                st.markdown(
                    f"""
                    <div style='
                        padding: 15px;
                        border-radius: 10px;
                        background-color: #ffffff;
                        margin: 8px 0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        border: 1px solid #e0e0e0;
                        height: 300px;
                    '>
                        <p style='
                            color: #666666;
                            font-size: 0.9em;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            margin-bottom: 8px;
                        '>{col}</p>
                        <div style='
                            height: calc(100% - 40px);
                            display: flex;
                            align-items: center;
                            justify-content: center;
                        '>
                            <p style='
                                color: #1f2937;
                                font-size: 1.6em;
                                font-weight: 600;
                                margin: 0;
                            '>{value}</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def display_overview_sheet(df):
    """Handle display of Overview sheet data"""
    # Create two columns for layout
    cols = st.columns(2)

    # Convert first two columns to dictionaries
    names = df.iloc[:, 0].tolist()
    values = df.iloc[:, 1].tolist()

    # Iterate through the pairs
    for i, (name, value) in enumerate(zip(names, values)):
        col_index = i % 2
        with cols[col_index]:
            # Format value if it's a float - round and add %
            if isinstance(value, float):
                if name == "Annual TIA Reward" or name == "Total Token":
                    value = f"{value:.0f}"
                elif name == "Target Yield %":
                    value = f"{value*100}%"
                else:
                    value = f"{value:.2f}%"
            st.markdown(
                f"""
                <div style='
                    padding: 15px;
                    border-radius: 10px;
                    background-color: #ffffff;
                    margin: 8px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                    border: 1px solid #e0e0e0;
                '>
                    <p style='
                        color: #666666;
                        font-size: 0.9em;
                        text-transform: uppercase;
                        letter-spacing: 0.5px;
                        margin-bottom: 8px;
                    '>{name}</p>
                    <p style='
                        color: #1f2937;
                        font-size: 1.6em;
                        font-weight: 600;
                        margin: 0;
                    '>{str(value)}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def app_model():
    # Initialize the loader
    loader = ExcelDataLoader()

    if not loader.excel_files:
        st.error("No Excel files found in the exels directory")
        return

    selected_file = st.selectbox(
        "Choose an Excel file",
        label_visibility="hidden",
        options=list(loader.excel_files.keys()),
        format_func=lambda x: x,  # Display the filename
    )

    # Load the selected file
    sheets = loader.load_data(loader.excel_files[selected_file])

    if not sheets:
        st.error(f"Error loading the selected file: {selected_file}")
        return

    # Create tabs for each sheet
    tabs = st.tabs(list(sheets.keys()))

    # Display data for each tab
    for tab, sheet_name in zip(tabs, sheets.keys()):
        with tab:
            st.header(sheet_name)
            if sheet_name == "Unlock":
                display_unlock_sheet(sheets[sheet_name])
            elif sheet_name == "Issuance":
                display_issuance_sheet(sheets[sheet_name])
            elif sheet_name == "Overview":
                display_overview_sheet(sheets[sheet_name])
            else:
                # Show regular dataframe for other sheets
                st.dataframe(sheets[sheet_name], use_container_width=True)


def display_unlock_sheet(df):
    """Handle display of Unlock sheet data"""
    st.subheader("Unlock Data by Month")

    # Display monthly/yearly/quarterly data
    monthly_tab, quarterly_tab, yearly_tab = st.tabs(
        ["Monthly View", "Quarterly View", "Yearly View"]
    )
    months = df["Month"].tolist()
    quarters = [int(month / 3) for month in months if month % 3 == 0]
    years = [int(month / 12 + 2023) for month in months if month % 12 == 0]

    with monthly_tab:
        selected_month = st.select_slider(
            "Select Month", options=months, key="monthly_month"
        )
        display_monthly_data(df, selected_month)

    with quarterly_tab:
        selected_quarter = st.select_slider(
            "Select Quarter", options=quarters, key="quarterly_quarter"
        )
        display_quarterly_data(df, selected_quarter)

    with yearly_tab:
        selected_year = st.select_slider(
            "Select Year", options=years, key="yearly_year"
        )
        display_yearly_data(df, (selected_year - 2023))

    # Split view for cumulative data and token distribution
    col1, col2 = st.columns(2)

    with col1:
        display_cumulative_data(df, months, quarters, years)

    with col2:
        display_token_distribution(df, months, quarters, years)

    # Display charts
    display_charts(df)


def display_cumulative_data(df, months, quarters, years):
    """Handle cumulative data display"""
    st.subheader("Cumulative Data")
    monthly_tab, quarterly_tab, yearly_tab = st.tabs(
        ["Monthly View", "Quarterly View", "Yearly View"]
    )

    with monthly_tab:
        selected_month = st.select_slider(
            "Select Month", options=months, key="cumulative_month"
        )
        display_latest_cumulative_data(df, selected_month)

    with quarterly_tab:
        selected_quarter = st.select_slider(
            "Select Quarter", options=quarters, key="cumulative_quarter"
        )
        display_latest_cumulative_data(df, selected_quarter * 3)

    with yearly_tab:
        selected_year = st.select_slider(
            "Select Year", options=years, key="cumulative_year"
        )
        display_latest_cumulative_data(df, (selected_year - 2023) * 12)


def display_token_distribution(df, months, quarters, years):
    """Handle token distribution display"""
    st.subheader("Token Distribution")
    monthly_tab, quarterly_tab, yearly_tab = st.tabs(
        ["Monthly View", "Quarterly View", "Yearly View"]
    )

    with monthly_tab:
        selected_month = st.select_slider(
            "Select Month", options=months, key="pie_month"
        )
        pie_fig = create_unlock_pie_chart(df, selected_month)
        st.plotly_chart(pie_fig, use_container_width=True, key="pie_chart_month")

    with quarterly_tab:
        selected_quarter = st.select_slider(
            "Select Quarter", options=quarters, key="pie_quarter"
        )
        pie_fig = create_unlock_pie_chart(df, selected_quarter * 3)
        st.plotly_chart(pie_fig, use_container_width=True, key="pie_quarter_chart")

    with yearly_tab:
        selected_year = st.select_slider("Select Year", options=years, key="pie_year")
        pie_fig = create_unlock_pie_chart(df, (selected_year - 2023) * 12)
        st.plotly_chart(pie_fig, use_container_width=True)


def display_charts(df):
    """Handle display of all charts"""
    charts = [
        ("Cumulative Unlock Schedule Plot", create_unlock_plot),
        ("Cumulative Unlock Schedule Chart", create_unlock_column_chart),
        ("Yearly Emission Schedule", create_unlock_emission_plot),
    ]

    for title, chart_func in charts:
        st.subheader(title)
        chart = chart_func(df)
        st.plotly_chart(chart, use_container_width=True)


def display_issuance_sheet(df):
    """Handle display of Issuance sheet data with dataframe and plots"""
    st.subheader("Issuance Data")

    # Display the dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    # Create two columns for the plots
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(create_relative_issuance_plot(df), use_container_width=True)

    with col2:
        st.plotly_chart(create_absolute_issuance_plot(df), use_container_width=True)

    st.plotly_chart(create_issuance_ratio_plot(df), use_container_width=True)


if __name__ == "__main__":
    app_model()
