from data_loader import load_data
from trend_detection import detect_trends

df = load_data("data/original_assignment_sample.csv")

trends = detect_trends(df, threshold=10)

print("\nDetected Trends:")
print(trends.to_string(index=False))
