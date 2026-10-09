from data_loader import load_data
from trend_detection import detect_trends
from outlier_detection import detect_outliers
from correlation import detect_correlations
from insight_generator import (
    generate_insights,
    export_insights
)

# Load dataset
df = load_data("data/original_assignment_sample.csv")

# Run analysis
trends = detect_trends(df, threshold=10)
outliers = detect_outliers(df)

corr_matrix, correlations = detect_correlations(
    df, threshold=0.70
)

# Generate explanations
insights = generate_insights(
    trends, outliers, correlations
)

print("\nGenerated Insights:")
print(insights.to_string(index=False))

print("\nTotal insights:", len(insights))

# Export results
export_insights(insights)
