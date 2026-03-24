import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, f1_score, classification_report

df = pd.read_csv("../Dataset/processed_dataset.csv")

FEATURES = [
    'Age', 'Weight',
    'Hypertension', 'Diabetes', 'BMI', 'Level',
    'Target Calories'
]
X = df[FEATURES]
y = df['Exercises']

class RandomForestModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=800,
            max_depth=30,
            min_samples_split=5,
            min_samples_leaf=2,
            max_features='sqrt',
            class_weight='balanced_subsample',
            bootstrap=True,
            oob_score=True,
            n_jobs=-1,
            random_state=42
        )

    def train(self, x, y):
        self.model.fit(x, y)

    def predict(self, data):
        return self.model.predict(data)

    def evaluate(self, x_test, y_test):
        y_pred = self.predict(x_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='macro')
        report = classification_report(y_test, y_pred, zero_division=0)
        return acc, f1, report

    def save(self, path="models/diet_model.pkl"):
        joblib.dump(self.model, path)

    def load(self, path="models/diet_model.pkl"):
        self.model = joblib.load(path)


x_train, x_test, y_train, y_test = train_test_split(
    X, y, stratify=y, test_size=0.2, random_state=42
)

model = RandomForestModel()
model.train(x_train, y_train)

# acc,_,_ = model.evaluate(x_test, y_test)
#
# plt.bar(['Accuracy'], [acc * 100], color='green', width=0.5)
# plt.ylabel('Accuracy (%)')
# plt.ylim(0, 100)
# plt.title('Random Forest Model Accuracy')
# plt.show()

# importances = pd.Series(model.model.feature_importances_, index=FEATURES)
# importances = importances.sort_values(ascending=True)
#
# plt.figure(figsize=(8, 5))
# plt.barh(importances.index, importances.values)
# plt.xlabel("Важност на характеристиката")
# plt.ylabel("Характеристика")
# plt.title("Feature Importances (Random Forest)")
# plt.tight_layout()
# plt.show()
model.save('exercise_model_rfc.pkl')

# acc, f1, report = model.evaluate(x_test, y_test)
# print("OOB score :", model.model.oob_score_)
# print("Accuracy  :", acc)
# print("Macro-F1  :", f1)
# print(report)

# cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
#
# rf_cv = RandomForestClassifier(
#     n_estimators=800,
#     max_depth=30,
#     min_samples_split=5,
#     min_samples_leaf=2,
#     max_features='sqrt',
#     class_weight='balanced_subsample',
#     bootstrap=True,
#     n_jobs=-1,
#     random_state=42
# )

# f1_scores  = cross_val_score(rf_cv, X, y, scoring='f1_macro', cv=cv, n_jobs=-1)
# acc_scores = cross_val_score(rf_cv, X, y, scoring='accuracy',  cv=cv, n_jobs=-1)
#
# print("\n5-fold CV results:")
# print(f"Macro-F1: {f1_scores.mean():.4f} ± {f1_scores.std():.4f}")
# print(f"Accuracy: {acc_scores.mean():.4f} ± {acc_scores.std():.4f}")

# model.save("models/diet_rf_final.pkl")


