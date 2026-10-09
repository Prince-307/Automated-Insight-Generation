
from data_loader import load_data
from outlier_detection import detect_outliers

df = load_data("data/original_assignment_sample.csv")

outliers = detect_outliers(df)

print("\nDetected Outliers:")

if outliers.empty:
    print("No outliers detected.")
else:
    print(outliers.to_string(index=False))
