import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd

df = pd.read_csv('../Dataset/processed_dataset.csv')


class TreeModel:
    def __init__(self):
        self.model = DecisionTreeClassifier()

    def train(self, x, y):
        self.model.fit(x,y)

    def predict(self, data):
        return self.model.predict(data)

    def evaluate(self, x_test, y_test):
        return self.model.score(x_test, y_test)

    def save(self, path='models/diet_model.pkl'):
        joblib.dump(self.model, path)

    def load(self, path='models/diet_model.pkl'):
        self.model = joblib.load(path)

x = df[[
    'Sex', 'Age', 'Height', 'Weight',
    'Hypertension', 'Diabetes', 'BMI', 'Level',
    'Activity Factor', 'BMR', 'TDEE', 'Target Calories'
]]

y = df['Exercises']


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

model = TreeModel()
model.train(x_train, y_train)

sample_input = {
    'Sex': 1,
    'Age': 28,
    'Height': 1.75,
    'Weight': 72,
    'Hypertension': 0,
    'Diabetes': 0,
    'BMI': 23.5,
    'Level': 1,
    'Activity Factor': 1.55,
    'BMR': 1650,
    'TDEE': 2557.5,
    'Target Calories': 2057.5
}

pred = model.predict(pd.DataFrame([sample_input]))

print(pred)


