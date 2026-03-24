import numpy as np
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib

df = pd.read_csv('../Dataset/processed_dataset.csv')


class MLPModel:
    def __init__(self):
        self.model = MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=1000, random_state=42)

    def train(self, x, y):
        self.model.fit(x, y)

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
    'Fitness Goal', 'Fitness Type', 'Exercises',
    'Activity Factor', 'BMR', 'TDEE', 'Target Calories'
]]

y = df['Diet']

total_accuracy_mlp = 0
for i in range(100):

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    model = MLPModel()
    model.train(x_train_scaled, y_train)

    accuracy = model.evaluate(x_test_scaled, y_test)

    total_accuracy_mlp += accuracy


