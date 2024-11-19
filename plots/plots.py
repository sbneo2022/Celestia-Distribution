import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from PIL import ImageColor

# Professional financial color palette
FINANCIAL_COLORS = [
    "#003f5c",  # Dark blue
    "#58508d",  # Purple
    "#bc5090",  # Pink
    "#ff6361",  # Coral
    "#ffa600",  # Orange
    "#374c80",  # Navy
    "#7a5195",  # Violet
    "#bc5090",  # Magenta
]


def create_unlock_plot(df: pd.DataFrame):
    # Filter only cumulative columns
    cumulative_cols = [
        col
        for col in df.columns
        if "Cumulative " in str(col) and "Emission" not in str(col)
    ]

    # Create the plot
    fig = go.Figure()

    # Custom colors - using a more vibrant palette
    colors = px.colors.qualitative.Pastel

    # Calculate total for percentage calculation
    total_series = df[cumulative_cols].sum(axis=1)

    # Add traces for each cumulative column
    for i, col in enumerate(cumulative_cols):
        # Fix percentage calculation
        percentage = [
            round((val / total) * 100, 2) if total != 0 else 0
            for val, total in zip(df[col], total_series)
        ]

        fig.add_trace(
            go.Scatter(
                x=df["Month"],
                y=df[col],
                name=col.replace("Cumulative ", ""),
                mode="lines",
                fill="tonexty",
                opacity=0.7,
                line=dict(
                    width=3,
                    color=FINANCIAL_COLORS[i % len(FINANCIAL_COLORS)],
                    shape="spline",
                ),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    + f"{col.replace('Cumulative ', '')}<br>"
                    + "Amount: %{y:,.0f} tokens<br>"
                    + "Share: %{customdata:.2f}%<br>"
                    + "<extra></extra>"
                ),
                customdata=percentage,
            )
        )

    # Update layout with improved styling
    fig.update_layout(
        title={
            "text": "Token Unlock Schedule",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=24, family="Arial Black", color="#2E4053"),
        },
        xaxis_title=dict(text="Month", font=dict(size=16, family="Arial")),
        yaxis_title=dict(text="Token Amount", font=dict(size=16, family="Arial")),
        height=700,
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1,
            font=dict(size=12, family="Arial"),
        ),
        plot_bgcolor="rgba(240,240,240,0.3)",
        paper_bgcolor="white",
        font=dict(size=14, family="Arial"),
        dragmode="zoom",  # Enable box zoom by default
        modebar=dict(
            bgcolor="rgba(255,255,255,0.7)", color="#2E4053", activecolor="#1f77b4"
        ),
    )

    # Enhanced grid lines and axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
        tickformat=",",  # Add thousand separators
    )

    # Add buttons for different zoom levels
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.7,
                y=1.08,
                showactive=True,
                buttons=list(
                    [
                        dict(
                            label="All Time",
                            method="relayout",
                            args=[{"xaxis.autorange": True, "yaxis.autorange": True}],
                        ),
                        dict(
                            label="1 Year",
                            method="relayout",
                            args=[
                                {
                                    "xaxis.range": [
                                        df["Month"].iloc[0],
                                        df["Month"].iloc[12],
                                    ]
                                }
                            ],
                        ),
                        dict(
                            label="2 Years",
                            method="relayout",
                            args=[
                                {
                                    "xaxis.range": [
                                        df["Month"].iloc[0],
                                        df["Month"].iloc[24],
                                    ]
                                }
                            ],
                        ),
                        dict(
                            label="3 Years",
                            method="relayout",
                            args=[
                                {
                                    "xaxis.range": [
                                        df["Month"].iloc[0],
                                        df["Month"].iloc[36],
                                    ]
                                }
                            ],
                        ),
                    ]
                ),
            )
        ]
    )

    return fig


def create_unlock_pie_chart(df: pd.DataFrame, selected_month=None):
    """Create an enhanced pie chart showing token distribution."""
    # Get data for selected month or latest
    if selected_month is not None:
        distribution = df[df["Month"] == selected_month].iloc[0]
    else:
        distribution = df.iloc[-1]

    # Filter for Cumulative columns
    cumulative_cols = [
        col
        for col in df.columns
        if "Cumulative " in str(col) and "Emission" not in str(col)
    ]

    # Custom color palette matching the line plot
    colors = FINANCIAL_COLORS

    # Prepare data
    values = []
    labels = []
    percentages = []  # Store calculated percentages

    # Process columns
    emission_value = 0
    for col in cumulative_cols:
        value = distribution[col]
        if "Emission" in col:
            emission_value = value
        else:
            label = col.replace("Cumulative ", "")
            values.append(value)
            labels.append(label)

    if emission_value > 0:
        values.append(emission_value)
        labels.append("Total Emission")

    # Calculate total and percentages
    total = sum(values)
    percentages = [f"{(value/total*100):.1f}%" for value in values]

    # Create enhanced pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.5,
                textinfo="label+text",
                textposition="inside",
                text=percentages,
                texttemplate="%{label}<br>%{text}",
                textfont=dict(size=12, color="white", family="Arial"),
                marker=dict(colors=colors, line=dict(color="white", width=2)),
                hovertemplate="<b>%{label}</b><br>"
                + "Amount: %{value:,.0f}<br>"
                + "Share: %{text}<br>"
                + "<extra></extra>",
                rotation=90,
                insidetextorientation="horizontal",
            )
        ]
    )

    # Add center text with total
    fig.add_annotation(
        text=f"Total<br>{total:,.0f}",
        x=0.5,
        y=0.5,
        font=dict(size=20, color="#2E4053", family="Arial Black"),
        showarrow=False,
    )

    # Update layout
    fig.update_layout(
        title=dict(
            text="Token Distribution",
            y=0.95,
            x=0.5,
            xanchor="center",
            yanchor="top",
            font=dict(size=24, color="#2E4053", family="Arial Black"),
        ),
        height=700,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(size=12, family="Arial"),
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1,
        ),
        margin=dict(t=80, b=80, l=20, r=20),
        paper_bgcolor="white",
        plot_bgcolor="white",
        uniformtext=dict(minsize=10, mode="hide"),
    )

    return fig


def create_unlock_column_chart(df: pd.DataFrame):
    """Create an enhanced column chart showing monthly token unlocks."""
    # Filter for non-cumulative columns
    unlock_cols = [
        col
        for col in df.columns
        if "Cumulative " in str(col)
        and "Month" not in str(col)
        and "Emission" not in str(col)
    ]

    # Professional financial color palette
    colors = FINANCIAL_COLORS

    # Create the plot
    fig = go.Figure()

    # Calculate total for percentage calculation
    total_series = df[unlock_cols].sum(axis=1)

    # Add bars for each unlock column
    for i, col in enumerate(unlock_cols):
        # Calculate percentage for each category
        percentage = [
            round((val / total) * 100, 2) if total != 0 else 0
            for val, total in zip(df[col], total_series)
        ]

        clean_name = col.replace("Cumulative ", "")
        fig.add_trace(
            go.Bar(
                x=df["Month"],
                y=df[col],
                name=clean_name,
                marker_color=colors[i % len(colors)],
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    + f"{clean_name}<br>"
                    + "Amount: %{y:,.0f} tokens<br>"
                    + "Share: %{customdata:.2f}%<br>"
                    + "<extra></extra>"
                ),
                customdata=percentage,
            )
        )

    # Calculate and add total line
    fig.add_trace(
        go.Scatter(
            x=df["Month"],
            y=total_series,
            name="Total",
            line=dict(color="rgba(0,0,0,0.7)", width=3, dash="dot"),
            hovertemplate=(
                "<b>Total</b><br>"
                + "Date: %{x}<br>"
                + "Amount: %{y:,.0f} tokens<br>"
                + "<extra></extra>"
            ),
        )
    )

    # Update layout with improved styling
    fig.update_layout(
        title={
            "text": "Monthly Token Unlocks by Category",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=24, family="Arial Black", color="#2E4053"),
        },
        xaxis_title=dict(text="Month", font=dict(size=16, family="Arial")),
        yaxis_title=dict(text="Token Amount", font=dict(size=16, family="Arial")),
        height=700,
        barmode="stack",
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1,
            font=dict(size=12, family="Arial"),
        ),
        plot_bgcolor="rgba(240,240,240,0.3)",
        paper_bgcolor="white",
        font=dict(size=14, family="Arial"),
        dragmode="zoom",
        modebar=dict(
            bgcolor="rgba(255,255,255,0.7)", color="#2E4053", activecolor="#1f77b4"
        ),
    )

    # Enhanced grid lines and axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
        tickformat=",",
    )

    # Add zoom buttons
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.7,
                y=1.08,
                showactive=True,
                buttons=list(
                    [
                        dict(
                            label="All Time",
                            method="relayout",
                            args=[{"xaxis.autorange": True, "yaxis.autorange": True}],
                        ),
                        dict(
                            label="1 Year",
                            method="relayout",
                            args=[
                                {
                                    "xaxis.range": [
                                        df["Month"].iloc[0],
                                        df["Month"].iloc[12],
                                    ]
                                }
                            ],
                        ),
                        dict(
                            label="2 Years",
                            method="relayout",
                            args=[
                                {
                                    "xaxis.range": [
                                        df["Month"].iloc[0],
                                        df["Month"].iloc[24],
                                    ]
                                }
                            ],
                        ),
                        dict(
                            label="3 Years",
                            method="relayout",
                            args=[
                                {
                                    "xaxis.range": [
                                        df["Month"].iloc[0],
                                        df["Month"].iloc[36],
                                    ]
                                }
                            ],
                        ),
                    ]
                ),
            )
        ]
    )

    return fig


def create_unlock_emission_plot(df: pd.DataFrame):
    # Filter only cumulative emission columns
    cumulative_cols = [col for col in df.columns if "Cumulative Emission" in str(col)]

    # Create the plot
    fig = go.Figure()

    # Professional financial color palette
    colors = FINANCIAL_COLORS

    # Calculate total for percentage calculation
    total_series = df[cumulative_cols].sum(axis=1)

    # Add traces for each cumulative column
    for i, col in enumerate(cumulative_cols):
        percentage = [
            round((val / total) * 100, 2) if total != 0 else 0
            for val, total in zip(df[col], total_series)
        ]

        fig.add_trace(
            go.Scatter(
                x=df["Month"],
                y=df[col],
                name=col.replace("Cumulative ", ""),
                mode="lines",
                fill="tonexty",  # Added area fill
                fillcolor=f"rgba{tuple(list(ImageColor.getrgb(colors[i % len(colors)])) + [0.1])}",
                line=dict(width=3, color=colors[i % len(colors)], shape="spline"),
                hovertemplate=(
                    "<b>%{x}</b><br>"
                    + f"{col.replace('Cumulative ', '')}<br>"
                    + "Amount: %{y:,.0f} tokens<br>"
                    + "Share: %{customdata:.1f}%<br>"
                    + "<extra></extra>"
                ),
                customdata=percentage,
            )
        )

    # Update layout with improved styling
    fig.update_layout(
        title={
            "text": "Yearly Token Emission Schedule",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=24, family="Arial Black", color="#2E4053"),
        },
        xaxis_title=dict(text="Month", font=dict(size=16, family="Arial")),
        yaxis_title=dict(text="Token Amount", font=dict(size=16, family="Arial")),
        height=700,
        hovermode="x unified",
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",  # Moved to right
            x=0.99,
            bgcolor="rgba(255, 255, 255, 0.9)",
            bordercolor="rgba(0,0,0,0.1)",
            borderwidth=1,
            font=dict(size=12, family="Arial"),
        ),
        plot_bgcolor="white",  # Clean white background
        paper_bgcolor="white",
        font=dict(size=14, family="Arial"),
        dragmode="zoom",
        margin=dict(t=100, r=100, b=50, l=50),  # Adjusted margins
    )

    # Lighter grid lines
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.1)",
        showline=True,
        linewidth=1,
        linecolor="rgba(0,0,0,0.2)",
        mirror=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.1)",
        showline=True,
        linewidth=1,
        linecolor="rgba(0,0,0,0.2)",
        mirror=True,
        tickformat=",",
    )

    return fig


def create_relative_issuance_plot(df):
    """Create relative issuance plot"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Relative Issuance %"],
            mode="lines",
            name="Relative Issuance",
            line=dict(color=FINANCIAL_COLORS[0], width=3, shape="spline"),  # Dark blue
            hovertemplate=(
                "<b>%{x}</b><br>" + "Relative Issuance: %{y}%<br>" + "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title={
            "text": "Relative Issuance Over Time",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=24, family="Arial Black", color="#2E4053"),
        },
        xaxis_title=dict(text="Date", font=dict(size=16, family="Arial")),
        yaxis_title=dict(
            text="Relative Issuance (%)", font=dict(size=16, family="Arial")
        ),
        height=700,
        hovermode="x unified",
        showlegend=False,
        plot_bgcolor="rgba(240,240,240,0.3)",
        paper_bgcolor="white",
        font=dict(size=14, family="Arial"),
        margin=dict(t=100, b=50, l=50, r=50),
    )

    # Enhanced axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
        tickformat=".2f",
    )

    return fig


def create_absolute_issuance_plot(df):
    """Create absolute issuance plot"""
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Absolute issuance %"],
            mode="lines",
            name="Absolute Issuance",
            line=dict(color=FINANCIAL_COLORS[1], width=3, shape="spline"),  # Purple
            hovertemplate=(
                "<b>%{x}</b><br>"
                + "Absolute Issuance: %{y:.4f}<br>"
                + "<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        title={
            "text": "Absolute Issuance Over Time",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=24, family="Arial Black", color="#2E4053"),
        },
        xaxis_title=dict(text="Date", font=dict(size=16, family="Arial")),
        yaxis_title=dict(text="Absolute Issuance", font=dict(size=16, family="Arial")),
        height=700,
        hovermode="x unified",
        showlegend=False,
        plot_bgcolor="rgba(240,240,240,0.3)",
        paper_bgcolor="white",
        font=dict(size=14, family="Arial"),
        margin=dict(t=100, b=50, l=50, r=50),
    )

    # Enhanced axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
        tickformat=".4f",  # Show 4 decimal places
    )

    return fig


def create_issuance_ratio_plot(df):
    """Create plot showing ratio between Relative and Absolute issuance"""
    fig = go.Figure()

    df["Issuance Ratio"] = df["Relative Issuance %"] / df["Absolute issuance %"]

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Issuance Ratio"],
            mode="lines",
            name="Issuance Ratio",
            line=dict(
                color="#003f5c",  # Professional financial blue
                width=3,
                shape="spline",  # Smooth line
            ),
            hovertemplate=(
                "<b>%{x}</b><br>" + "Ratio: %{y:.4f}<br>" + "<extra></extra>"
            ),
        )
    )

    # Update layout with improved styling
    fig.update_layout(
        title={
            "text": "Issuance Ratio Over Time",
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": dict(size=24, family="Arial Black", color="#2E4053"),
        },
        xaxis_title=dict(text="Date", font=dict(size=16, family="Arial")),
        yaxis_title=dict(text="Ratio", font=dict(size=16, family="Arial")),
        height=700,
        hovermode="x unified",
        showlegend=False,  # Hide legend since there's only one trace
        plot_bgcolor="rgba(240,240,240,0.3)",
        paper_bgcolor="white",
        font=dict(size=14, family="Arial"),
        margin=dict(t=100, b=50, l=50, r=50),
    )

    # Enhanced grid lines and axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
    )

    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(128,128,128,0.2)",
        showline=True,
        linewidth=2,
        linecolor="rgba(0,0,0,0.3)",
        mirror=True,
        tickformat=".4f",  # Show 4 decimal places
    )

    return fig
