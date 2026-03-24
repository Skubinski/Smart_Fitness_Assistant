import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd
import matplotlib.pyplot as plt

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
    'Height', 'Weight',
    'Hypertension', 'Diabetes', 'BMI', 'Level',
    'Exercises',
    'Target Calories'
]]

y = df['Diet']


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

model = TreeModel()
model.train(x_train, y_train)

accuracy = model.evaluate(x_test,y_test)

print(accuracy * 100)

# plt.bar(['Accuracy'], [accuracy * 100], color='green', width=0.5)
# plt.ylabel('Accuracy (%)')
# plt.ylim(0, 100)
# plt.title('Tree Model Accuracy')
# plt.show()
# importances = pd.Series(model.model.feature_importances_, index=x.columns)
# importances = importances.sort_values(ascending=False)
# print(importances)
# model.save('diet_model.pkl')

