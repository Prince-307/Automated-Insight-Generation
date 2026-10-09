import pandas as pd
import plotly.express as px
import streamlit as st

from correlation import detect_correlations
from data_loader import load_data
from insight_generator import generate_insights
from outlier_detection import detect_outliers
from trend_detection import detect_trends

st.set_page_config(
    page_title="Automated Insight Generation",
    page_icon="📊",
    layout="wide",
)

st.title("Automated Insight Generation")
st.caption(
    "Healthcare data analysis, trend detection, "
    "outlier detection and correlation analysis"
)

# Upload CSV
uploaded_file = st.file_uploader(
    "Upload healthcare CSV",
    type=["csv"],
)

if uploaded_file is not None:
    try:
        df = load_data(uploaded_file)
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        st.stop()

    indicators = [
        "anc_coverage",
        "institutional_delivery",
        "immunization",
        "high_risk_cases",
    ]

    df["month_str"] = df["month"].dt.strftime("%Y-%m")

    # Sidebar Filters
    st.sidebar.header("Filters & Parameters")

    # 1. District Filter
    all_districts = sorted(df["district"].unique())
    selected_districts = st.sidebar.multiselect(
        "Select districts",
        all_districts,
        default=all_districts,
    )

    # 2. Month Filter
    all_months = sorted(df["month_str"].dropna().unique())
    selected_months = st.sidebar.multiselect(
        "Select months",
        all_months,
        default=all_months,
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("Detection Thresholds")

    # Trend threshold
    trend_threshold = st.sidebar.slider(
        "Trend threshold (%)",
        min_value=1,
        max_value=50,
        value=10,
        help="Flag percentage changes exceeding this threshold.",
    )

    # Outlier detection method & threshold
    outlier_method = st.sidebar.selectbox(
        "Outlier detection method",
        ["IQR", "Z-score"],
        index=0,
    )

    if outlier_method == "IQR":
        outlier_threshold = st.sidebar.slider(
            "IQR multiplier threshold",
            min_value=0.5,
            max_value=3.0,
            value=1.5,
            step=0.1,
            help="Default is 1.5 * IQR.",
        )
    else:
        outlier_threshold = st.sidebar.slider(
            "Z-score threshold (|z|)",
            min_value=1.0,
            max_value=4.0,
            value=3.0,
            step=0.1,
            help="Default is 3.0 standard deviations.",
        )

    # Correlation threshold
    correlation_threshold = st.sidebar.slider(
        "Correlation threshold (|r|)",
        min_value=0.50,
        max_value=1.00,
        value=0.70,
        step=0.05,
        help="Flag strong Pearson correlations above this magnitude.",
    )

    # Filtered dataframe
    filtered_df = df[
        df["district"].isin(selected_districts)
        & df["month_str"].isin(selected_months)
    ].copy()

    if filtered_df.empty:
        st.warning("No data available for the selected district/month filters.")
        st.stop()

    # Run analysis on filtered data
    trends = detect_trends(
        filtered_df, threshold=trend_threshold
    )

    outliers = detect_outliers(
        filtered_df,
        method=outlier_method.lower(),
        threshold=outlier_threshold,
    )

    corr_matrix, correlations = detect_correlations(
        filtered_df,
        threshold=correlation_threshold,
    )

    insights = generate_insights(
        trends, outliers, correlations
    )

    # Summary cards
    st.subheader("Analysis Summary")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Rows", len(filtered_df))
    c2.metric("Trend Insights", len(trends))
    c3.metric("Outliers", len(outliers))
    c4.metric("Strong Correlations", len(correlations))

    # Dataset preview
    with st.expander("View filtered dataset"):
        st.dataframe(
            filtered_df.drop(columns=["month_str"], errors="ignore"),
            width="stretch",
        )

    # Visualizations Section
    st.subheader("Healthcare Visualizations")

    col_left, col_right = st.columns(2)

    with col_left:
        selected_indicator = st.selectbox(
            "Choose indicator to visualize",
            indicators,
        )

        chart_data = filtered_df.sort_values("month")

        line_fig = px.line(
            chart_data,
            x="month",
            y=selected_indicator,
            color="district",
            markers=True,
            title=f"{selected_indicator} over time",
        )
        st.plotly_chart(line_fig, width="stretch")

    with col_right:
        # Severity Counts Bar Chart
        if not insights.empty and "severity" in insights.columns:
            severity_counts = (
                insights["severity"]
                .value_counts()
                .reindex(["High", "Medium", "Low"], fill_value=0)
                .reset_index()
            )
            severity_counts.columns = ["Severity", "Count"]

            bar_fig = px.bar(
                severity_counts,
                x="Severity",
                y="Count",
                color="Severity",
                color_discrete_map={
                    "High": "#ef4444",
                    "Medium": "#f59e0b",
                    "Low": "#10b981",
                },
                title="Insight Severity Distribution",
            )
            st.plotly_chart(bar_fig, width="stretch")
        else:
            st.info("No insights to display in severity chart.")

    # Correlation Heatmap
    st.subheader("Correlation Analysis")

    if len(filtered_df) < 10:
        st.caption(
            "⚠️ **Statistical Note:** Small sample size (less than 10 observations). "
            "Pearson correlations on small samples may be unstable."
        )

    heatmap_fig = px.imshow(
        corr_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        title="Pearson Correlation Heatmap",
    )
    st.plotly_chart(heatmap_fig, width="stretch")

    # Insights Table & Exports
    st.subheader("Generated Automated Insights")

    if insights.empty:
        st.info("No insights detected for the current filter settings.")
    else:
        st.dataframe(insights, width="stretch")

        b1, b2, b3 = st.columns(3)
        with b1:
            st.download_button(
                "📥 Download Insights CSV",
                data=insights.to_csv(index=False),
                file_name="generated_insights.csv",
                mime="text/csv",
            )
        with b2:
            st.download_button(
                "📥 Download Insights JSON",
                data=insights.to_json(orient="records", indent=2),
                file_name="generated_insights.json",
                mime="application/json",
            )
        with b3:
            st.download_button(
                "📥 Download Correlation Matrix",
                data=corr_matrix.to_csv(),
                file_name="correlation_matrix.csv",
                mime="text/csv",
            )

else:
    st.info("Upload your healthcare CSV to begin.")
    st.write(
        "The engine will calculate month-over-month trends, "
        "identify outliers via IQR/Z-score, examine Pearson correlations, "
        "and generate structured explanations automatically."
    )

