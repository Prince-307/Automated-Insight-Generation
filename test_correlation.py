from data_loader import load_data
from correlation import detect_correlations

df = load_data("data/original_assignment_sample.csv")

corr_matrix, correlations = detect_correlations(
    df, threshold=0.70
)

print("\nPearson Correlation Matrix:")
print(corr_matrix.round(3))

print("\nStrong Correlations:")

if correlations.empty:
    print("No strong correlations detected.")
else:
    print(correlations.to_string(index=False))

# Export correlation matrix
corr_matrix.to_csv("correlation_matrix.csv")

print("\nCorrelation matrix exported successfully.")
