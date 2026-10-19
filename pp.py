
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report
)
from sklearn.impute import SimpleImputer

# =====================================
# 1. LOAD DATASET
# =====================================

df = pd.read_csv(
    r"D:\fsd\student_placement_raw.csv"
)

df.columns = df.columns.str.strip().str.lower()

print("Dataset shape:", df.shape)

# Remove duplicates
df = df.drop_duplicates().copy()

# =====================================
# 2. CLEAN TARGET
# =====================================

df["placed"] = (
    df["placed"].astype("string")
    .str.strip()
    .str.lower()
)

df["placed"] = df["placed"].map({
    "yes": 1,
    "no": 0,
    "1": 1,
    "0": 0
})

df = df.dropna(subset=["placed"])
df["placed"] = df["placed"].astype(int)

# =====================================
# 3. SELECT FEATURES
# =====================================

# Student ID should not be used for prediction
X = df.drop(
    columns=["placed", "student_id"],
    errors="ignore"
)

y = df["placed"]

numeric_features = [
    "cgpa",
    "aptitude_score",
    "coding_score",
    "projects",
    "internships",
    "communication_score",
    "backlogs"
]

categorical_features = ["branch"]

# Convert numerical columns
for col in numeric_features:
    X[col] = pd.to_numeric(
        X[col], errors="coerce"
    )

# Treat invalid values as missing
ranges = {
    "cgpa": (0, 10),
    "aptitude_score": (0, 100),
    "coding_score": (0, 100),
    "projects": (0, None),
    "internships": (0, None),
    "communication_score": (0, 100),
    "backlogs": (0, None)
}

for col, (low, high) in ranges.items():
    invalid = X[col] < low

    if high is not None:
        invalid |= X[col] > high

    X.loc[invalid, col] = np.nan

# Clean branch column
X["branch"] = (
    X["branch"]
    .astype("object")
    .str.strip()
    .str.upper()
)

# Convert missing values into np.nan
X["branch"] = X["branch"].replace(
    ["", "NAN", "NONE", "<NA>"],
    np.nan
)

# Ensure standard object dtype
X["branch"] = X["branch"].astype(object)

# =====================================
# 4. TRAIN-TEST SPLIT
# =====================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# =====================================
# 5. HANDLE MISSING VALUES
# =====================================

num_imputer = SimpleImputer(strategy="median")
cat_imputer = SimpleImputer(strategy="most_frequent")

X_train = X_train.copy()
X_test = X_test.copy()

X_train[numeric_features] = num_imputer.fit_transform(
    X_train[numeric_features]
)

X_test[numeric_features] = num_imputer.transform(
    X_test[numeric_features]
)

X_train[categorical_features] = cat_imputer.fit_transform(
    X_train[categorical_features].astype(object)
)

X_test[categorical_features] = cat_imputer.transform(
    X_test[categorical_features].astype(object)
)

valid_branches = sorted(
    X_train["branch"].unique().tolist()
)

# =====================================
# 6. ONE-HOT ENCODING
# =====================================

X_train = pd.get_dummies(
    X_train,
    columns=["branch"],
    dtype=int
)

X_test = pd.get_dummies(
    X_test,
    columns=["branch"],
    dtype=int
)

X_test = X_test.reindex(
    columns=X_train.columns,
    fill_value=0
)

feature_names = X_train.columns.tolist()

# =====================================
# 7. TRAIN RANDOM FOREST
# =====================================

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    min_samples_split=5,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("\nModel training completed!")

# =====================================
# 8. TEST MODEL
# =====================================

y_pred = model.predict(X_test)

print("\nAccuracy:",
      round(accuracy_score(y_test, y_pred) * 100, 2),
      "%")

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred, labels=[0, 1]))

print("\nClassification Report:")
print(classification_report(
    y_test, y_pred,
    labels=[0, 1],
    target_names=["Not Placed", "Placed"],
    zero_division=0
))

# =====================================
# 9. FEATURE IMPORTANCE
# =====================================

importance = pd.DataFrame({
    "Feature": feature_names,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:")
print(importance.to_string(index=False))

# =====================================
# 10. NEW STUDENT PREDICTION
# =====================================

print("\n--- New Student Prediction ---")

student = {}

for col in numeric_features:

    while True:
        try:
            value = float(input(f"Enter {col}: "))

            low, high = ranges[col]

            if not np.isfinite(value):
                print("Enter a finite number.")
                continue

            if value < low or (
                high is not None and value > high
            ):
                print("Value outside valid range!")
                continue

            if col in ["projects", "internships", "backlogs"]:
                if not value.is_integer():
                    print("Enter a whole number.")
                    continue

            student[col] = value
            break

        except ValueError:
            print("Enter a valid number.")

print("\nAvailable branches:", valid_branches)

while True:
    branch = input("Enter branch: ").strip().upper()

    if branch in valid_branches:
        student["branch"] = branch
        break

    print("Invalid branch. Choose from the list.")

new_df = pd.DataFrame([student])

# Apply the SAME categorical encoding
new_df = pd.get_dummies(
    new_df,
    columns=["branch"],
    dtype=int
)

new_df = new_df.reindex(
    columns=feature_names,
    fill_value=0
)

prediction = model.predict(new_df)[0]
probability = model.predict_proba(new_df)[0]

placed_index = list(model.classes_).index(1)
placed_probability = probability[placed_index]

print("\n-----------------------------")

if prediction == 1:
    print("Prediction: PLACED")
else:
    print("Prediction: NOT PLACED")

print(
    "Estimated placement probability:",
    round(placed_probability * 100, 2),
    "%"
)

print("-----------------------------")
