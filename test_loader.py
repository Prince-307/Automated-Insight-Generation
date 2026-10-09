from data_loader import load_data

df = load_data(
    "data/original_assignment_sample.csv"
)

print("\nData loaded successfully!")
print("Total rows:", len(df))
print("Total districts:", df["district"].nunique())
